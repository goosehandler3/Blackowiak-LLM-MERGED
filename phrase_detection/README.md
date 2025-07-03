# Phrase Detection Feature — README

## Overview

The phrase detection feature aims to enhance the custom LLM therapy note application by identifying repetitive phrases, canned language, and overused patterns that could reduce note quality or trigger insurance audits. By proactively detecting these patterns, clinicians can revise notes to improve clinical integrity and avoid flags.

---

## Goals

- Detect exact and near-duplicate phrases within individual notes and across multiple notes.  
- Identify common “canned” phrases and alert clinicians.  
- Provide actionable, clear feedback for revision.  
- Integrate seamlessly into the existing LLM session processing pipeline.  
- Offer configuration options to tune sensitivity and phrase libraries.  
- Present results effectively within the GUI for immediate clinician use.

---

## Technical Roadmap

### 1. Data Collection & Baseline Analysis

- Gather diverse sample therapy notes.  
- Analyze to identify typical repetitive and canned phrases.  
- Build a baseline dataset for detection heuristics.

### 2. Phrase Detection Module

- Implement using text similarity measures such as:  
  - Levenshtein distance  
  - Jaccard similarity  
  - Cosine similarity with TF-IDF vectors  
- Detect exact duplicates and near-duplicates.  
- Establish frequency thresholds and ignore lists.

### 3. Integration with LLM Pipeline

- Incorporate detection as a pre- or post-processing step in session note generation.  
- Automatically analyze generated notes for repetition.  
- Return structured feedback for GUI display.

### 4. Feedback and Reporting

- Create detailed reports listing:  
  - Repetitive phrases detected  
  - Frequency counts and locations  
  - Suggested rewrites or flags for review

### 5. Configuration and Tuning

- Use YAML or JSON config files for:  
  - Phrases to flag or ignore  
  - Sensitivity and threshold levels  
- Enable live updates without code changes.

### 6. Testing & Validation

- Unit tests on synthetic and real notes.  
- User feedback loops to refine false positives/negatives.  
- Continuous integration with CI tools for regression prevention.

### 7. Documentation and Training

- Detailed technical docs on module usage and config.  
- Clinician guides for interpreting feedback and adjusting thresholds.  
- Example notes and test cases for developers.

---

## File Structure
<pre>
```
/phrase_detection/
├── detector.py         # Core detection algorithms and functions
├── config.yaml         # Configurable phrase lists and thresholds
├── utils.py            # Text processing helpers
├── tests/              # Unit and integration tests
│   └── test_detector.py
├── examples/           # Sample therapy notes and outputs
│   └── sample_note.txt
└── README.md           # This file
```
</pre>


---

## GUI Integration and Implications

The phrase detection feature will affect the user interface in the following ways:

- **Real-time Feedback:** As users write or generate session notes, the GUI should display alerts or highlights when repetitive or canned phrases are detected.
  
- **Summary Dashboard:** A dedicated panel or modal to review flagged phrases, their counts, and suggested alternatives.

- **Configurable Settings:** Interface elements to adjust detection sensitivity, add/remove flagged phrases, and toggle notifications.

- **Performance Considerations:** Efficient asynchronous processing to avoid UI lag during live detection.

- **Integration Points:** Ensure seamless interaction between the phrase detection module and existing components like the LLM output preview and save workflows.
⸻

Contribution and Collaboration

This roadmap serves as a guide for ongoing development and refinement of phrase detection in the LLM therapy note app. Contributions, testing feedback, and enhancements—both for detection accuracy and user experience—are encouraged to ensure clinical utility and audit resilience.

---

## Sample Code Snippet

```python
import re
from collections import Counter
from typing import List, Tuple

class PhraseDetector:
    def __init__(self, ignore_phrases: List[str] = None):
        self.ignore_phrases = ignore_phrases or []

    def detect_repetitive_phrases(self, text: str, min_phrase_length: int = 4, threshold: int = 2) -> List[Tuple[str, int]]:
        """
        Detect repeated phrases in the text.
        
        Args:
            text: The therapy note text.
            min_phrase_length: Minimum number of words in phrase to detect.
            threshold: Minimum times phrase must repeat to flag.
        
        Returns:
            List of tuples: (repeated phrase, count)
        """
        # Split text into words, normalize
        words = re.findall(r'\b\w+\b', text.lower())
        phrases = []

        # Extract all phrases of length >= min_phrase_length
        for i in range(len(words) - min_phrase_length + 1):
            phrase = ' '.join(words[i:i+min_phrase_length])
            if phrase not in self.ignore_phrases:
                phrases.append(phrase)

        counts = Counter(phrases)
        repetitive = [(phrase, count) for phrase, count in counts.items() if count >= threshold]
        return repetitive

# Usage example
detector = PhraseDetector(ignore_phrases=["client states", "reported feeling"])
text = "Client states feeling tired. Client states feeling tired and stressed. Client states feeling tired."
repeats = detector.detect_repetitive_phrases(text)
print(repeats)
# Output: [('client states feeling tired', 3)]
