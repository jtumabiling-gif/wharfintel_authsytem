/**
 * Password Validation Utility
 * Implements secure password strength checking with detailed requirements
 */

export const passwordRequirements = {
  lowercase: {
    label: 'At least one lowercase letter',
    pattern: /[a-z]/,
    weight: 1
  },
  uppercase: {
    label: 'At least one uppercase letter',
    pattern: /[A-Z]/,
    weight: 1
  },
  digit: {
    label: 'At least one digit',
    pattern: /[0-9]/,
    weight: 1
  },
  symbol: {
    label: 'At least one special character (!@#$%^&*...)',
    pattern: /[!@#$%^&*()_+\-=\[\]{};:'",.< >?/\\|`~]/,
    weight: 1
  },
  minLength: {
    label: 'Minimum 12 characters',
    pattern: /.{12,}/,
    weight: 2
  }
};

/**
 * Validate password against all requirements
 * Returns detailed information about strength and what's missing
 */
export const validatePassword = (password) => {
  const results = {
    lowercase: passwordRequirements.lowercase.pattern.test(password),
    uppercase: passwordRequirements.uppercase.pattern.test(password),
    digit: passwordRequirements.digit.pattern.test(password),
    symbol: passwordRequirements.symbol.pattern.test(password),
    minLength: passwordRequirements.minLength.pattern.test(password)
  };

  const metCount = Object.values(results).filter(Boolean).length;
  const totalCount = Object.keys(results).length;

  // Calculate strength score (0-100)
  let score = 0;
  if (results.lowercase) score += 20;
  if (results.uppercase) score += 20;
  if (results.digit) score += 20;
  if (results.symbol) score += 20;
  if (results.minLength) score += 20;

  // Determine strength level
  let strength = 'Weak';
  let strengthColor = 'weak';
  let isValid = false;

  if (metCount === 5) {
    strength = 'Strong';
    strengthColor = 'strong';
    isValid = true;
  } else if (metCount >= 3) {
    strength = 'Medium';
    strengthColor = 'medium';
    isValid = false;
  } else {
    strength = 'Weak';
    strengthColor = 'weak';
    isValid = false;
  }

  return {
    strength,
    strengthColor,
    score,
    isValid,
    metCount,
    totalCount,
    requirements: results,
    message: getStrengthMessage(strength, isValid)
  };
};

/**
 * Get user-friendly message based on strength
 */
const getStrengthMessage = (strength, isValid) => {
  const messages = {
    'Strong': '✓ Password meets all security requirements',
    'Medium': '⚠ Password is acceptable but could be stronger',
    'Weak': '✗ Password is too weak'
  };
  return messages[strength] || messages['Weak'];
};

/**
 * Check if two passwords match
 */
export const passwordsMatch = (password, confirmPassword) => {
  return password === confirmPassword && password.length > 0;
};

/**
 * Get missing requirements
 */
export const getMissingRequirements = (validationResults) => {
  const missing = [];
  
  if (!validationResults.requirements.lowercase) {
    missing.push(passwordRequirements.lowercase.label);
  }
  if (!validationResults.requirements.uppercase) {
    missing.push(passwordRequirements.uppercase.label);
  }
  if (!validationResults.requirements.digit) {
    missing.push(passwordRequirements.digit.label);
  }
  if (!validationResults.requirements.symbol) {
    missing.push(passwordRequirements.symbol.label);
  }
  if (!validationResults.requirements.minLength) {
    missing.push(passwordRequirements.minLength.label);
  }
  
  return missing;
};

/**
 * Generate example password
 */
export const generateExamplePassword = () => {
  return "Cyber@2026Secure";
};
