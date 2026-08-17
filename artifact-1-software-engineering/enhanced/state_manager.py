#
# state_manager.py - This file manages the valid machine states and
# controls all state transitions for the Raspberry Pi application.
# It keeps state validation separate from serial communication and
# hardware control.
#
#------------------------------------------------------------------
# Change History
#------------------------------------------------------------------
# Version   |   Description
#------------------------------------------------------------------
#    1          Initial Enhanced Development
#------------------------------------------------------------------

from typing import FrozenSet


class StateManager:
    # Maintains the current state and validates requested transitions.

    VALID_STATES: FrozenSet[str] = frozenset({
        "Running",
        "Idle",
        "Soft Error",
        "Hard Error",
    })

    def __init__(self, initial_state: str = "Idle") -> None:
        if initial_state not in self.VALID_STATES:
            raise ValueError(f"Invalid initial state: {initial_state}")

        self._current_state = initial_state

    @property
    def current_state(self) -> str:
        # Returns the current system state.
        return self._current_state

    def is_valid_state(self, state: str) -> bool:
        # Returns True when the supplied state is supported.
        return state in self.VALID_STATES

    def transition_to(self, new_state: str) -> bool:
        # Changes the current state when the requested state is valid and
        # different from the current state.
        #
        # Returns:
        #     True when a state change occurred.
        #     False when the system was already in the requested state.
        if not self.is_valid_state(new_state):
            raise ValueError(f"Invalid state: {new_state}")

        if new_state == self._current_state:
            return False

        self._current_state = new_state
        return True
