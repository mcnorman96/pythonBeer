import type { fetchHelperType, fetchingOptionsType } from '@/types/types';
import { checkTokenExpired } from '@/utils/authUtil';

export const fetchHelper = async ({
  path,
  method = 'GET',
  body = null,
  checkToken = true,
}: fetchHelperType) => {
  const fetchOptions: fetchingOptionsType = {
    method: method,
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${localStorage.getItem('token')}`,
    },
  };

  if (method !== 'GET' && body) {
    fetchOptions.body = JSON.stringify(body);
  }

  const res = await fetch(path, fetchOptions);

  const data = await res.json();

  if (checkToken) checkTokenExpired(res.status, data.error);

  if (!res.ok) {
    return { success: false, error: data.error };
  }

  return { success: true, response: data.response, message: data.message };
};
