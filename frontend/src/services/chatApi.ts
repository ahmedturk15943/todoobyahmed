/**
 * Chat API client for frontend.
 * Handles communication with the backend chat endpoint.
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface ChatRequest {
  conversation_id?: number;
  message: string;
}

export interface ChatResponse {
  conversation_id: number;
  response: string;
  tool_calls: Array<{
    tool: string;
    parameters: Record<string, any>;
    result: Record<string, any>;
  }>;
}

export interface ChatError {
  detail: string;
}

/**
 * Send a message to the AI chatbot.
 *
 * @param userId - Authenticated user ID
 * @param request - Chat request with message and optional conversation_id
 * @returns Chat response with assistant's reply
 * @throws Error if request fails
 */
export async function sendMessage(
  userId: string,
  request: ChatRequest
): Promise<ChatResponse> {
  try {
    const response = await fetch(`${API_URL}/api/${userId}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      const error: ChatError = await response.json();
      throw new Error(error.detail || 'Failed to send message');
    }

    const data: ChatResponse = await response.json();
    return data;
  } catch (error) {
    console.error('Chat API error:', error);
    throw error;
  }
}

/**
 * Get user's conversations.
 *
 * @param userId - Authenticated user ID
 * @returns List of conversations
 */
export async function getConversations(userId: string): Promise<any[]> {
  try {
    const response = await fetch(`${API_URL}/api/${userId}/conversations`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error('Failed to fetch conversations');
    }

    return await response.json();
  } catch (error) {
    console.error('Failed to fetch conversations:', error);
    return [];
  }
}
