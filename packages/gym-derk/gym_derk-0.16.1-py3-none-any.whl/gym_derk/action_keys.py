from enum import Enum

class ActionKeys(Enum):
  """These are the actions a Derkling can take, which you send to the step function.

  Attributes:
    MoveX = 0: A number between -1 and 1
    Rotate = 1: A number between -1 and 1
    ChaseFocus = 2: A number between 0 and 1
    CastingSlot = 3: 0=don't cast. 1-3=cast corresponding ability
    ChangeFocus = 4: 0=keep current focus. 1=focus home statue. 2-3=focus teammates, 4=focus enemy statue, 5-7=focus enemy
  """
  MoveX = 0
  Rotate = 1
  ChaseFocus = 2
  CastingSlot = 3
  ChangeFocus = 4
