export const checkTokenExpired = (statusCode: number, error: string) => {
  if (statusCode === 401 && error === 'Token has expired') {
    localStorage.removeItem('token');
    window.location.href = '/login';
    throw new Error('Token expired');
  }
  return false;
}
