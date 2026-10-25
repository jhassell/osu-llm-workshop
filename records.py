"""The record every document becomes. One row of the table the afternoon searches.

Every value carries where it came from: the document id, the source file, and
a short excerpt copied from the document that supports the main claim. A value
the document does not state is written as "not stated", never guessed.

Change the two marked lines in Module 3 to add the one column your field needs.
"""
from pydantic import BaseModel, Field


class Record(BaseModel):
    doc_id: str = Field(description="The document id given in the prompt, copied exactly.")
    source: str = Field(description="The source file name given in the prompt, copied exactly.")
    title: str = Field(description="The document's title, or 'not stated'.")
    year: str = Field(description="Four-digit year of the work, or 'not stated'.")
    method: str = Field(description="One of: experimental, computational, theoretical, qualitative, review, mixed.")
    sample_size: str = Field(description="How many samples, subjects, specimens, or runs, with the unit, or 'not stated'.")
    main_claim: str = Field(description="The main finding in one sentence, in the document's own terms.")
    excerpt: str = Field(description="A sentence copied word for word from the document that supports main_claim.")

    # ---- Your column. Change these two marked lines (Module 3). ----
    # Three worked examples:
    #   organism: str = Field(description="The organism or system studied, or 'not stated'.")
    #   instrument: str = Field(description="The main instrument or technique named, or 'not stated'.")
    #   dataset: str = Field(description="The dataset or benchmark used, or 'not stated'.")
    custom_field: str = Field(description="Fill this in with what your field needs, or 'not stated'.")  # EDIT 1: rename custom_field
    # EDIT 2: write its description above.


FIELDS = list(Record.model_fields)
