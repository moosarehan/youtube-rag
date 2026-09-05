'use client';

import { useState } from 'react';

type Message = {
  role: 'user' | 'assistant';
  content: string;
  sources?: Array<{
    video_id: string;
    title: string;
    timestamp: number;
  }>;
};

export default function Home() {
  const [videoUrl, setVideoUrl] = useState('');
  const [sessionId, setSessionId] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isIngesting, setIsIngesting] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const handleIngest = async () => {
    if (!videoUrl.trim()) return;

    setIsIngesting(true);
    try {
      const response = await fetch('http://localhost:8000/api/ingest', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: videoUrl }),
      });

      const data = await response.json();
      
      if (response.ok) {
        setSessionId(data.session_id);
        setMessages([]);
        alert(`Video ingested successfully! Session ID: ${data.session_id}`);
      } else {
        alert(`Error: ${data.detail || 'Failed to ingest video'}`);
      }
    } catch (error) {
      alert('Failed to connect to the backend');
      console.error(error);
    } finally {
      setIsIngesting(false);
    }
  };

  const handleSendMessage = async () => {
    if (!input.trim() || !sessionId) return;

    const userMessage: Message = { role: 'user', content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: sessionId,
          question: input,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        const assistantMessage: Message = {
          role: 'assistant',
          content: data.answer,
          sources: data.sources,
        };
        setMessages((prev) => [...prev, assistantMessage]);
      } else {
        alert(`Error: ${data.detail || 'Failed to get response'}`);
      }
    } catch (error) {
      alert('Failed to connect to the backend');
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 py-8 max-w-6xl">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
            YouTube RAG Chat
          </h1>
          <p className="text-gray-600 dark:text-gray-300">
            Ask questions about any YouTube video
          </p>
        </div>

        {/* Video Input Section */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
            1. Add YouTube Video
          </h2>
          <div className="flex gap-2">
            <input
              type="text"
              value={videoUrl}
              onChange={(e) => setVideoUrl(e.target.value)}
              placeholder="Paste YouTube URL here..."
              className="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white"
              disabled={isIngesting}
            />
            <button
              onClick={handleIngest}
              disabled={isIngesting || !videoUrl.trim()}
              className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors font-medium"
            >
              {isIngesting ? 'Processing...' : 'Ingest Video'}
            </button>
          </div>
          {sessionId && (
            <p className="mt-2 text-sm text-green-600 dark:text-green-400">
              ✓ Session active: {sessionId}
            </p>
          )}
        </div>

        {/* Chat Section */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden">
          <div className="p-6 border-b border-gray-200 dark:border-gray-700">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
              2. Ask Questions
            </h2>
          </div>

          {/* Messages */}
          <div className="h-96 overflow-y-auto p-6 space-y-4">
            {messages.length === 0 && (
              <div className="text-center text-gray-500 dark:text-gray-400 py-12">
                {sessionId
                  ? 'Start asking questions about the video!'
                  : 'Ingest a video first to start chatting'}
              </div>
            )}

            {messages.map((message, index) => (
              <div
                key={index}
                className={`flex ${
                  message.role === 'user' ? 'justify-end' : 'justify-start'
                }`}
              >
                <div
                  className={`max-w-3xl rounded-lg px-4 py-2 ${
                    message.role === 'user'
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white'
                  }`}
                >
                  <p className="whitespace-pre-wrap">{message.content}</p>
                  {message.sources && message.sources.length > 0 && (
                    <div className="mt-2 pt-2 border-t border-gray-300 dark:border-gray-600">
                      <p className="text-xs font-semibold mb-1">Sources:</p>
                      {message.sources.map((source, idx) => (
                        <div key={idx} className="text-xs">
                          • {source.title} (
                          <a
                            href={`https://www.youtube.com/watch?v=${source.video_id}&t=${Math.floor(source.timestamp)}s`}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="underline hover:text-blue-400"
                          >
                            {Math.floor(source.timestamp)}s
                          </a>
                          )
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            ))}

            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-gray-100 dark:bg-gray-700 rounded-lg px-4 py-2">
                  <p className="text-gray-500 dark:text-gray-400">
                    Thinking...
                  </p>
                </div>
              </div>
            )}
          </div>

          {/* Input */}
          <div className="p-4 border-t border-gray-200 dark:border-gray-700">
            <div className="flex gap-2">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                placeholder={
                  sessionId
                    ? 'Ask a question...'
                    : 'Ingest a video first...'
                }
                className="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white"
                disabled={!sessionId || isLoading}
              />
              <button
                onClick={handleSendMessage}
                disabled={!sessionId || !input.trim() || isLoading}
                className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors font-medium"
              >
                Send
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
