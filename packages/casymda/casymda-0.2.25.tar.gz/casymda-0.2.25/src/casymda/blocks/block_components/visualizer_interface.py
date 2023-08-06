from abc import abstractmethod

from casymda.blocks.block_components.state import States
from casymda.blocks.entity import Entity


class BlockVisualizer:
    """visualizer called from the visualizable_block"""

    @abstractmethod
    def animate_block(self, block, queuing_direction_x=None):
        raise NotImplementedError()

    @abstractmethod
    def change_block_state(self, block, state: States, new_value: bool):
        raise NotImplementedError()

    @abstractmethod
    def animate_entity_flow(self, entity: Entity, from_block, to_block):
        """animate_entity_flow
        destroy entity if to_block is None"""
        raise NotImplementedError()
