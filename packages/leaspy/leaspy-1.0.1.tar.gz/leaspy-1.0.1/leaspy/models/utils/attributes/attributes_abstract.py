import torch


# TODO 2 : Add some individual attributes -> Optimization on the w_i = A * s_i
class AttributesAbstract:
    """
    Contains the common attributes & methods of the different attributes classes.
    Such classes are used to update the models' attributes.

    Parameters
    ----------
    dimension: `int` (default None)
    source_dimension: `int` (default None)

    Attributes
    ----------
    dimension: `int`
    source_dimension: `int`
    betas: `torch.Tensor`, (default None)
    mixing_matrix: `torch.Tensor`, (default None)
        Matrix A such that w_i = A * s_i.
    positions: `torch.Tensor`, (default None)
        Previously noted "g".
    orthonormal_basis: `torch.Tensor`, (default None)
    velocities: `torch.Tensor`, (default None)
        Previously noted "v0".
    name: `str` (default None)
        Name of the associated leaspy model. Used by ``update`` method.
    update_possibilities: `tuple` [`str`], (default ('all', 'g', 'v0', 'betas') )
        Contains the available parameters to update. Different models have different parameters.

    Methods
    -------
    get_attributes()
        Returns the following attributes: ``positions``, ``velocities`` & ``mixing_matrix``.
    update(names_of_changed_values, values)
        Update model group average parameter(s).
    """

    def __init__(self, dimension=None, source_dimension=None):
        """
        Instantiate a AttributesAbstract class object.
        """
        self.dimension = dimension
        self.source_dimension = source_dimension

        self.betas = None
        self.mixing_matrix = None
        self.orthonormal_basis = None
        self.positions = None
        self.velocities = None

        self.name = None
        self.update_possibilities = ('all', 'g', 'v0', 'betas')

    def get_attributes(self):
        """
        Returns the following attributes: ``positions``, ``velocities`` & ``mixing_matrix``.

        Returns
        -------
        - positions: `torch.Tensor`
        - velocities: `torch.Tensor`
        - mixing_matrix: `torch.Tensor`
        """
        return self.positions, self.velocities, self.mixing_matrix

    def update(self, names_of_changed_values, values):
        """
        Update model group average parameter(s).

        Parameters
        ----------
        names_of_changed_values: `list` [`str`]
            Must be one of - "all", "g", "v0", "betas". Raise an error otherwise.
            "g" correspond to the attribute ``positions``.
            "v0" correspond to the attribute ``velocities``.
        values: `dict` [`str`, `torch.Tensor`]
            New values used to update the model's group average parameters
        """
        self._check_names(names_of_changed_values)

        compute_betas = False
        compute_deltas = False
        compute_positions = False
        compute_velocities = False

        if 'all' in names_of_changed_values:
            names_of_changed_values = self.update_possibilities  # make all possible updates

        if 'betas' in names_of_changed_values:
            compute_betas = True
        if 'deltas' in names_of_changed_values:
            compute_deltas = True
        if 'g' in names_of_changed_values:
            compute_positions = True
        if ('v0' in names_of_changed_values) or ('xi_mean' in names_of_changed_values):
            compute_velocities = True

        if compute_betas:
            self._compute_betas(values)
        if compute_deltas:
            self._compute_deltas(values)
        if compute_positions:
            self._compute_positions(values)
        if compute_velocities:
            self._compute_velocities(values)

        # TODO : Check if the condition is enough
        if (compute_positions or compute_velocities) and (self.name != 'univariate'):
            self._compute_orthonormal_basis()
        if (compute_positions or compute_velocities or compute_betas) and (self.name != 'univariate'):
            self._compute_mixing_matrix()

    def _check_names(self, names_of_changed_values):
        """
        Check if the name of the parameter(s) to update are in the possibilities allowed by the model.

        Parameters
        ----------
        names_of_changed_values: `list` [`str`]

        Raises
        -------
        ValueError
        """
        def raise_err(name):
            raise ValueError("The name {} is not in the attributes that are used to be updated".format(name))
        [raise_err(n) for n in names_of_changed_values if n not in self.update_possibilities]

    def _compute_positions(self, values):
        """
        Update the attribute ``positions``.

        Parameters
        ----------
        values: `dict` [`str`, `torch.Tensor`]
        """
        self.positions = torch.exp(values['g'])

    def _compute_velocities(self, values):
        """
        Update the attribute ``velocities``.

        Parameters
        ----------
        values: `dict` [`str`, `torch.Tensor`]
        """
        self.velocities = torch.exp(values['v0'])

    def _compute_betas(self, values):
        """
        Update the attribute ``betas``.

        Parameters
        ----------
        values: `dict` [`str`, `torch.Tensor`]
        """
        if self.source_dimension == 0:
            return
        self.betas = values['betas'].clone()

    def _compute_deltas(self, values):
        raise NotImplementedError

    def _compute_orthonormal_basis(self):
        """
        Compute the attribute ``orthonormal_basis`` which is a basis orthogonal to velocities v0 for the inner product
        implied by the metric. It is equivalent to be a base orthogonal to v0 / (p0^2 (1-p0)^2 for the euclidean norm.
        """
        raise NotImplementedError

    def _compute_Q(self, dgamma_t0):
        """
        Used in non-abstract attributes classes to compute the ``orthonormal_basis`` attribute given the
        differentiation of the geodesic at initial time.

        Parameters
        ----------
        dgamma_t0: `torch.Tensor`
        """
        e1 = torch.zeros(self.dimension)
        e1[0] = 1
        alpha = torch.sign(dgamma_t0[0]) * torch.norm(dgamma_t0)
        u_vector = dgamma_t0 - alpha * e1
        v_vector = u_vector / torch.norm(u_vector)
        v_vector = v_vector.reshape(1, -1)

        q_matrix = torch.eye(self.dimension) - 2 * v_vector.permute(1, 0) * v_vector
        self.orthonormal_basis = q_matrix[:, 1:]

    @staticmethod
    def _mixing_matrix_utils(linear_combination_values, matrix):
        """
        Intermediate function used to test the good behaviour of the class' methods.

        Parameters
        ----------
        linear_combination_values: `torch.Tensor`
        matrix: `torch.Tensor`

        Returns
        -------
        `torch.Tensor`
        """
        return torch.mm(matrix, linear_combination_values)

    def _compute_mixing_matrix(self):
        """
        Update the attribute ``mixing_matrix``.
        """
        if self.source_dimension == 0:
            return
        self.mixing_matrix = self._mixing_matrix_utils(self.betas, self.orthonormal_basis)
