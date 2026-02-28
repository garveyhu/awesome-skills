export const HttpStatus = {
  OK: {
    code: 1,
    message: 'OK',
  },
  SUCCESS: {
    code: 200,
    message: 'Success',
  },
  BAD_REQUEST: {
    code: 400,
    message: 'Bad Request',
  },
  UNAUTHORIZED: {
    code: 401,
    message: 'Unauthorized',
  },
  FORBIDDEN: {
    code: 403,
    message: 'Forbidden',
  },
  NOT_FOUND: {
    code: 404,
    message: 'Not Found',
  },
  REQUEST_TIMEOUT: {
    code: 408,
    message: 'Request Timeout',
  },
  SERVER_ERROR: {
    code: 500,
    message: 'Internal Server Error',
  },
  SERVICE_UNAVAILABLE: {
    code: 503,
    message: 'Service Unavailable',
  },
} as const;
