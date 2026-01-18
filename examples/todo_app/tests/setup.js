import '@testing-library/jest-dom';

// Mock window.alert
global.alert = jest.fn();

// Mock window.confirm
global.confirm = jest.fn(() => true);

// Mock fetch for API calls
global.fetch = jest.fn();
