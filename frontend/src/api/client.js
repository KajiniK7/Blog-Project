import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const MODERATION_TIMEOUT_MS = 180000;

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

/**
 * Creates a new draft post.
 * @param {{ title: string, content: string }} postData
 * @returns {Promise<any>}
 */
export const createPost = async (postData) => {
  const response = await apiClient.post('/posts/', postData);
  return response.data;
};

/**
 * Submits an existing post (draft or flagged) for AI moderation review.
 * @param {number|string} postId
 * @returns {Promise<{ id: number, status: string, reasons: string[], message: string }>}
 */
export const submitPost = async (postId) => {
  const response = await apiClient.post(
    `/posts/${postId}/submit/`,
    undefined,
    { timeout: MODERATION_TIMEOUT_MS }
  );
  return response.data;
};

/**
 * Lists posts, optionally filtered by status ('draft', 'flagged', 'approved', 'published') and scoped by currentUser.
 * @param {string|null} [status]
 * @param {string|null} [currentUser]
 * @returns {Promise<any[]>}
 */
export const listPosts = async (status = null, currentUser = null) => {
  const params = {};
  if (status && status !== 'all') {
    params.status = status.toLowerCase();
  }
  if (currentUser) {
    params.current_user = currentUser;
  }
  const response = await apiClient.get('/posts/', { params });
  return response.data;
};

/**
 * Publishes an approved post. Once published, the post becomes immutable.
 * @param {number|string} postId
 * @returns {Promise<any>}
 */
export const publishPost = async (postId) => {
  const response = await apiClient.patch(`/posts/${postId}/publish/`);
  return response.data;
};

/**
 * Retrieves full details for a single post by ID.
 * @param {number|string} postId
 * @returns {Promise<any>}
 */
export const getPost = async (postId) => {
  const response = await apiClient.get(`/posts/${postId}`);
  return response.data;
};

/**
 * Updates an existing post's title and/or content.
 * The backend resets the post status back to 'draft' after an edit.
 * @param {number|string} postId
 * @param {{ title?: string, content?: string }} postData
 * @returns {Promise<any>}
 */
export const updatePost = async (postId, postData) => {
  const response = await apiClient.put(`/posts/${postId}/`, postData);
  return response.data;
};

/**
 * Registers a new user.
 * @param {{ username: string, password: string }} credentials
 * @returns {Promise<any>}
 */
export const registerUser = async (credentials) => {
  const response = await apiClient.post('/auth/register/', credentials);
  return response.data;
};

/**
 * Logs in an existing user.
 * @param {{ username: string, password: string }} credentials
 * @returns {Promise<any>}
 */
export const loginUser = async (credentials) => {
  const response = await apiClient.post('/auth/login/', credentials);
  return response.data;
};

export default apiClient;


