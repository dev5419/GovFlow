from fastapi import Depends, HTTPException, status
from src.database.models.user import UserModel

# Stubbed for MVP. In a real environment with FastAPI-Users, 
# this would be provided by fastapi_users.current_user(active=True)
async def get_current_active_user() -> UserModel:
    # For MVP, we return a mock user representing a Procurement Officer
    # In reality, this relies on JWT Bearer transport and DB lookup
    return UserModel(
        id="mock_officer_123",
        email="officer@govflow.gov",
        role="Procurement Officer"
    )

async def require_role(allowed_roles: list[str]):
    async def role_checker(user: UserModel = Depends(get_current_active_user)):
        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role {user.role} is not authorized for this action. Required: {allowed_roles}"
            )
        return user
    return role_checker

# Pre-configured dependency for Procurement Officers (and Admins)
get_current_procurement_officer = require_role(["Procurement Officer", "System Administrator"])
