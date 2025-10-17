# Getting Support

Welcome to the Voice Assistant Demo community! We're here to help you learn and succeed with this project.

## 📚 Learning Resources

### Documentation
- **[README.md](README.md)** - Complete setup and usage guide
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Development guidelines and contribution process
- **Code Examples** - See the `src/voice_assistant/` directory for well-documented code

### Educational Focus
This project is designed as **training material** for learning modern Python development. We prioritize:
- Clear, educational explanations
- Patient help for learners at all levels
- Practical examples and use cases

## 🤝 Community Support

### GitHub Discussions (Recommended)
For questions, ideas, and community interaction:
- **[GitHub Discussions](https://github.com/yourusername/voice-assistant-demo/discussions)**
- Categories available:
  - 💡 **Ideas** - Feature suggestions and brainstorming
  - 🙋 **Q&A** - Questions and answers
  - 📢 **Show and Tell** - Share your projects and modifications
  - 💬 **General** - Open discussion about the project

### GitHub Issues
For specific problems:
- **[Bug Reports](https://github.com/yourusername/voice-assistant-demo/issues/new?template=bug_report.md)** - Something isn't working
- **[Feature Requests](https://github.com/yourusername/voice-assistant-demo/issues/new?template=feature_request.md)** - Suggest improvements

## 🚀 Quick Help

### Common Questions

**Q: How do I get started?**
A: Follow the [Quick Start](README.md#quick-start) guide in the README. Make sure you have PortAudio installed and an OpenAI API key.

**Q: The wake word isn't being detected**
A: Try increasing the ambient noise calibration time with `--ambient-noise-duration 2.0` or use a different wake word with `--keyword "computer"`.

**Q: I'm getting PyAudio installation errors**
A: Install PortAudio first (see [Installing PortAudio](README.md#installing-portaudio)) and ensure you have the necessary build tools.

**Q: How can I contribute?**
A: Check out our [Contributing Guide](CONTRIBUTING.md) for detailed instructions on setting up your development environment and submitting changes.

### Before Asking for Help

1. **Check the documentation** - README.md covers most common scenarios
2. **Search existing issues** - Your question might already be answered
3. **Try the troubleshooting section** - See [Troubleshooting](README.md#troubleshooting) in the README
4. **Enable debug logging** - Run with `--log-level DEBUG` for more information

## 🐛 Reporting Issues

### Bug Reports
Use our [bug report template](.github/ISSUE_TEMPLATE/bug_report.md) and include:
- Clear description of the problem
- Steps to reproduce
- Expected vs. actual behavior
- Environment details (OS, Python version, etc.)
- Error messages or logs

### Feature Requests
Use our [feature request template](.github/ISSUE_TEMPLATE/feature_request.md) and include:
- Clear use case description
- Detailed explanation of the desired behavior
- Why this would be valuable for learning/education

## 🎓 Educational Support

### For Instructors and Workshop Leaders
- This project is designed for educational use
- Feel free to modify and adapt for your teaching needs
- Consider contributing improvements back to help other educators
- Contact maintainers for bulk educational licensing questions

### For Students and Learners
- Don't hesitate to ask "beginner" questions - we welcome all skill levels
- Share your learning journey and modifications
- Help other students when you can
- Focus on understanding concepts, not just getting code to work

## 📞 Contact Information

### Maintainers
- Primary contact through GitHub issues and discussions
- For security vulnerabilities, see [SECURITY.md](SECURITY.md)
- For educational partnerships or bulk usage, open a discussion

### Response Times
- **GitHub Discussions**: Usually within 1-2 days
- **Bug Reports**: Within 2-3 days for initial response
- **Feature Requests**: Within 1 week for initial feedback
- **Security Issues**: Within 48 hours (see [SECURITY.md](SECURITY.md))

## 🌟 Community Guidelines

Please follow our [Code of Conduct](CODE_OF_CONDUCT.md) in all interactions. We strive to maintain a welcoming, inclusive, and educational environment.

### What We Encourage
- ✅ Asking questions and seeking help
- ✅ Sharing learning experiences and modifications
- ✅ Helping other community members
- ✅ Providing constructive feedback
- ✅ Contributing improvements and fixes

### What We Don't Support
- ❌ Commercial support or consulting
- ❌ Custom development requests
- ❌ Issues with heavily modified versions
- ❌ Non-educational commercial usage questions

## 🔧 Self-Help Resources

### Debugging Tips
1. **Enable verbose logging**: `--log-level DEBUG`
2. **Test components individually**: Try just speech recognition or just OpenAI API
3. **Check environment variables**: Ensure `OPENAI_API_KEY` is set correctly
4. **Verify dependencies**: Run `uv run pytest` to check if everything is working

### Development Environment
- Use `uv` for dependency management (much faster than pip)
- Run tests with `uv run pytest -v`
- Format code with `uv run ruff format .`
- Check code quality with `uv run ruff check .`

### Useful Commands
```bash
# Check if everything is working
uv run pytest -v

# Debug mode with verbose output
uv run voice-assistant --log-level DEBUG --once

# Test just the OpenAI integration
uv run python -c "from voice_assistant import VoiceAssistant; print('Import successful')"
```

---

## 💝 Thank You

Thank you for being part of the Voice Assistant Demo community! Your questions, contributions, and feedback help make this a better learning resource for everyone.

**Happy coding and learning!** 🎉
