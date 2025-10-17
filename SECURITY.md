# Security Policy

## Supported Versions

The following versions of Voice Assistant Demo are currently supported with security updates:

| Version | Supported          | Notes |
| ------- | ------------------ | ----- |
| 0.1.x   | :white_check_mark: | Current development version |
| < 0.1   | :x:                | Pre-release versions not supported |

## Security Considerations

This project is designed as **training material** and includes several security considerations:

### API Key Management
- **Never commit API keys** to version control
- Use environment variables for sensitive credentials
- The demo uses OpenAI API keys which should be kept secure
- Consider using API key rotation for production deployments

### Audio Processing
- Microphone access is required for functionality
- Audio data is processed locally and sent to external APIs (Google Speech Recognition, OpenAI)
- No audio data is stored locally by default
- Be aware of privacy implications when using voice data

### Dependencies
- Regular dependency updates are recommended
- Monitor security advisories for PyAudio, OpenAI SDK, and other dependencies
- Use `uv` for reproducible builds with locked dependencies

### Network Security
- The application makes HTTPS requests to:
  - Google Speech Recognition API
  - OpenAI API
  - Google Text-to-Speech API
- Ensure network connections are secure in production environments

## Reporting a Vulnerability

If you discover a security vulnerability in Voice Assistant Demo, please report it responsibly:

### For Security Issues:
1. **Do NOT open a public GitHub issue** for security vulnerabilities
2. Email the maintainers directly (if available) or create a private security advisory
3. Include detailed information about the vulnerability:
   - Description of the issue
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if known)

### Response Timeline:
- **Initial response**: Within 48 hours of report
- **Status update**: Weekly updates on investigation progress
- **Resolution**: Target 30 days for fix and disclosure

### What to Expect:
- **Accepted vulnerabilities**: We will work on a fix and coordinate disclosure
- **Declined reports**: We will explain why the issue doesn't qualify as a security vulnerability
- **Credit**: Security researchers will be credited in release notes (unless they prefer anonymity)

## Security Best Practices for Users

When using this project:

1. **Environment Setup**:
   - Use virtual environments to isolate dependencies
   - Keep dependencies updated with `uv lock --upgrade`
   - Review dependency security advisories

2. **API Key Security**:
   - Store API keys in environment variables, not code
   - Use separate API keys for development and production
   - Monitor API key usage for unusual activity
   - Rotate keys regularly

3. **Privacy Considerations**:
   - Be aware that voice data is sent to external services
   - Consider privacy implications in sensitive environments
   - Review terms of service for Google and OpenAI APIs

4. **Production Deployment**:
   - This is a demo project - additional hardening needed for production
   - Implement proper logging and monitoring
   - Consider rate limiting and error handling
   - Review and test all security configurations

## Scope

This security policy applies to:
- The main `voice-assistant-demo` repository
- Official releases and tags
- Documentation and examples

This policy does not cover:
- Third-party dependencies (report to their respective maintainers)
- User modifications or forks
- Issues in development/testing environments that don't affect the main codebase

---

**Note**: This project is intended for educational purposes. Additional security measures should be implemented before using in production environments.
