from app.services.machines.state_machine import ErrorState

LOGIN_NOT_FOUND = ErrorState(code=1, message="Login not found")
CENTERS_NOT_FOUND = ErrorState(code=2, message="Centers not found")
CATEGORIES_NOT_FOUND = ErrorState(code=3, message="Categories not found")
DATES_NOT_FOUND = ErrorState(code=4, message="Dates not found")

ARGS_NOT_FOUND = ErrorState(code=5, message="Args not found")
