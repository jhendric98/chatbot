# Pull Request

## Description

**Summary**
Briefly describe what this PR does and why.

**Type of change**
Please delete options that are not relevant:

- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Code refactoring (no functional changes)
- [ ] Performance improvement
- [ ] Test improvements

## Related Issues

### Fixes/Closes

- Fixes #[issue number]
- Closes #[issue number]

### Related

- Related to #[issue number]
- Part of #[issue number]

## Changes Made

### Detailed description

Provide a more detailed description of the changes:

- What was changed?
- Why was it changed?
- How was it implemented?

### Files modified

List the main files that were changed:

- `src/voice_assistant/assistant.py` - Added new feature X
- `tests/test_assistant.py` - Added tests for feature X
- `README.md` - Updated documentation

## Testing

### Test coverage

- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] I have tested the changes manually

### Testing performed

Describe the testing you performed:

```bash
# Commands used for testing
uv run pytest -v
uv run voice-assistant --test-new-feature
```

### Test results

- All tests pass: [ ] Yes [ ] No
- Coverage maintained/improved: [ ] Yes [ ] No [ ] N/A
- Manual testing successful: [ ] Yes [ ] No [ ] N/A

## Code Quality

### Linting and formatting

- [ ] I have run `uv run ruff check .` and fixed any issues
- [ ] I have run `uv run ruff format .` to format the code
- [ ] My code follows the project's style guidelines

### Code review

- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation

## Documentation

### Documentation updates

- [ ] I have updated the README.md if needed
- [ ] I have updated docstrings for new/modified functions
- [ ] I have added/updated code comments where necessary
- [ ] I have updated the CHANGELOG.md

**Examples**
If this adds new functionality, provide usage examples:

```python
# Example of new feature usage
from voice_assistant import VoiceAssistant

assistant = VoiceAssistant()
result = assistant.new_feature()
```

## Educational Impact

### Learning value

How does this change enhance the educational value of the project?

- [ ] Demonstrates new Python concepts
- [ ] Improves code clarity and readability
- [ ] Adds instructional comments or examples
- [ ] Enhances the learning experience

### Complexity level

- [ ] Beginner-friendly (easy to understand)
- [ ] Intermediate (requires some Python knowledge)
- [ ] Advanced (for experienced developers)

## Backward Compatibility

### Breaking changes

- [ ] This PR introduces breaking changes
- [ ] This PR is fully backward compatible
- [ ] This PR adds new optional functionality

### Migration guide

If there are breaking changes, provide migration instructions:

```bash
# How to update existing usage
# Old way:
old_command

# New way:
new_command
```

## Checklist

### Before submitting

- [ ] My code follows the style guidelines of this project
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] Any dependent changes have been merged and published

### Quality assurance

- [ ] I have tested this change thoroughly
- [ ] I have considered edge cases and error conditions
- [ ] I have verified that the change works as expected
- [ ] I have checked that no existing functionality is broken

## Screenshots/Recordings

**Visual changes**
If applicable, add screenshots or recordings to demonstrate the changes:

- Before: [screenshot/recording]
- After: [screenshot/recording]

## Additional Notes

**Implementation details**
Any additional context, implementation notes, or considerations:

**Future work**
Any follow-up work or related improvements that could be made:

**Questions for reviewers**
Specific questions or areas where you'd like reviewer feedback:

---

**Note**: This project prioritizes educational value and code clarity. Please ensure your changes maintain the project's focus on being a great learning resource.
