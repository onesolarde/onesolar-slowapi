
import time
from typing import Any

from app.schemas import InverterResponse


class GridConnectionService:
    """
    Manage the connection of a solar park to the power grid.
    """

    def disconnect_park_from_grid(self, solar_park_id: int) -> None:
        # Imagine this method interacts with the hardware to disconnect the solar park from the grid
        print(f"Disconnecting solar park {solar_park_id} from grid")

    def reconnect_park_to_grid(self, solar_park_id: int) -> None:
        # Imagine this method interacts with the hardware to reconnect the solar park to the grid
        print(f"Reconnecting solar park {solar_park_id} to grid")

    def check_for_software_updates(self, inverter_id: int) -> str:
        # Imagine this method checks if there are software updates available for the inverter
        print(f"Checking for software updates for inverter {inverter_id}")
        return "2.0.4"

    def update_inverter_software(self, inverter_id: int, new_version: str) -> None:
        # Imagine this method interacts with the hardware to update the inverter software
        print(f"Updating inverter {inverter_id} to software version {new_version}")
    
    def update_inverters(self) -> list[InverterResponse]:
        """
        Update all inverters of the solar park if a software update is available.
        TODO: implement this function after your 15 minutes of code review are up
        """
        raise NotImplementedError("This function is not implemented yet")

    def write_report(self, solar_park_id: int, updated_inverters: list[InverterResponse]) -> None:
        """
        Write a maintenance report for the solar park after performing maintenance.
        """
        # Gather necessary data for the report
        report_data = self.gather_report_data(solar_park_id)

        # get signature from maintenance manager
        self.get_signature(report_data, updated_inverters, manager_id=1)

    def gather_report_data(self, solar_park_id: int) -> dict[str, Any]:
        # Imagine this method gathers all necessary data for the maintenance report
        print(f"Gathering report data for solar park {solar_park_id}")
        return {"energy_output": 1000, "inverter_status": "OK"}
    
    def get_signature(self, report_data: dict[str, Any], updated_inverters: list[InverterResponse], manager_id: int):
        """
        Get a signature from the maintenance manager to approve the maintenance report.
        This might take a while, as he is often on vacation.
        """
        signature_received = False
        while not signature_received:
            print(f"Waiting for signature from manager {manager_id}...")
            # Imagine we check for the signature every 10 seconds
            time.sleep(10)
            # For the sake of this example, let's assume we receive the signature after 30 seconds
            signature_received = self.fetch_signature_status(manager_id)

        report_data["signature"] = f"Signature from manager {manager_id} for inverters {[inverter.id for inverter in updated_inverters]}"

    def fetch_signature_status(self, manager_id: int) -> bool:
        # Imagine this method checks if the signature from the maintenance manager has been received
        # ... check signature status ...
        return True if time.time() % 30 < 10 else False  # Simulate receiving signature after 30 seconds


grid_connection_service = GridConnectionService()