// Mock for ESM-only until-async package
module.exports = {
  until: async (fn) => {
    const maxAttempts = 50;
    const delay = 100;
    
    for (let i = 0; i < maxAttempts; i++) {
      try {
        const result = await fn();
        if (result) return result;
      } catch (e) {
        // Continue trying
      }
      await new Promise(resolve => setTimeout(resolve, delay));
    }
    throw new Error('Timeout waiting for condition');
  }
};
