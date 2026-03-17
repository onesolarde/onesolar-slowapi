
class PowerManagementService:
    """
    Manage the power of a solar park.
    """

    def restart_park(self, solar_park_id: int) -> None:
        # Imagine this method interacts with the hardware to restart the solar park
        print(f"Restarting solar park {solar_park_id}")


power_management_service = PowerManagementService()