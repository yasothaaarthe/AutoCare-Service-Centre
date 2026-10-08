# ============================================================
# vehicle_module.py
# AutoCare Service Centre Management System
# ============================================================


class Vehicle:
    """
    Parent class representing a standard vehicle.
    """

    def __init__(
        self,
        owner_name,
        phone,
        registration_no,
        model,
        year,
        service_charges=None
    ):
        self.owner_name = owner_name
        self.phone = phone
        self.registration_no = registration_no
        self.model = model
        self.year = year

        if service_charges is None:
            self.service_charges = {}
        else:
            self.service_charges = service_charges

    def add_service(self, service_name, charge):
        """
        Add a service and its charge to the vehicle.
        """
        self.service_charges[service_name] = float(charge)

    def total_charge(self):
        """
        Calculate total service charge for this vehicle.
        """
        return sum(self.service_charges.values())

    def __str__(self):
        """
        Magic method that returns a readable
        representation of the Vehicle object.
        """
        return (
            f"Owner: {self.owner_name}\n"
            f"Phone: {self.phone}\n"
            f"Registration No.: {self.registration_no}\n"
            f"Vehicle Model: {self.model}\n"
            f"Vehicle Year: {self.year}"
        )

    def __add__(self, other):
        """
        Operator overloading.

        Adds the total service charges of two
        Vehicle objects.
        """
        if not isinstance(other, Vehicle):
            return NotImplemented

        return self.total_charge() + other.total_charge()


class PremiumVehicle(Vehicle):
    """
    Subclass of Vehicle demonstrating inheritance.
    """

    def __init__(
        self,
        owner_name,
        phone,
        registration_no,
        model,
        year,
        service_charges=None,
        membership="Gold"
    ):
        # Call parent class constructor
        super().__init__(
            owner_name,
            phone,
            registration_no,
            model,
            year,
            service_charges
        )

        self.membership = membership

    def premium_benefit(self):
        """
        Returns the benefits available to premium customers.
        """
        return "Priority service and complimentary vehicle inspection."

    def __str__(self):
        """
        Override the parent's __str__ method.
        """
        return (
            f"Owner: {self.owner_name}\n"
            f"Phone: {self.phone}\n"
            f"Registration No.: {self.registration_no}\n"
            f"Vehicle Model: {self.model}\n"
            f"Vehicle Year: {self.year}\n"
            f"Vehicle Type: Premium Vehicle\n"
            f"Membership: {self.membership}"
        )