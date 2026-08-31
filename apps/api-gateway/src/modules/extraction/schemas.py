from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from govflow_shared_types import ExtractedField

# The endpoint will directly return List[ExtractedField] as per requirements.
# If we need a paginated or wrapped response in the future, we can add it here.
