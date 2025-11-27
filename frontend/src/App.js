import React, { useState, useRef, useEffect, useCallback } from "react";
import { SunIcon, MoonIcon, PaperAirplaneIcon, StopIcon, SparklesIcon, UserIcon, ChevronDownIcon } from "@heroicons/react/24/solid";

// Function to format markdown-style text
const formatMarkdown = (text) => {
  text = text.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
  text = text.replace(/\*(.+?)\*/g, '<em>$1</em>');
  return text;
};

// Available Gemini models
const GEMINI_MODELS = {
  'gemini-2.0-flash-exp': { name: 'Gemini 2.0 Flash', description: 'Fast & efficient' },
  'gemini-exp-1206': { name: 'Gemini Experimental', description: 'Latest features' },
  'gemini-2.5-flash': { name: 'Gemini 2.5 Flash', description: 'Balanced' },
  'gemini-pro': { name: 'Gemini Pro', description: 'Most capable' }
};

function App() {
  const [message, setMessage] = useState("");
  const [selectedModel, setSelectedModel] = useState(() => {
    const saved = localStorage.getItem("selectedModel");
    return saved || 'gemini-2.0-flash-exp';
  });
  const [showModelDropdown, setShowModelDropdown] = useState(false);
  const [chatLog, setChatLog] = useState(() => {
    try {
      const saved = localStorage.getItem("chatLog");
      return saved ? JSON.parse(saved).map(msg => ({...msg, timestamp: new Date(msg.timestamp)})) : [];
    } catch { return []; }
  });
  
  const [loading, setLoading] = useState(false);
  const [botTypingText, setBotTypingText] = useState("");
  const [darkMode, setDarkMode] = useState(() => {
    const saved = localStorage.getItem("darkMode");
    return saved ? JSON.parse(saved) : true;
  });

  const [userMemory] = useState(() => {
    try {
      const saved = localStorage.getItem("userMemory");
      return saved ? JSON.parse(saved) : {};
    } catch { return {}; }
  });

  const chatBoxRef = useRef(null);
  const abortControllerRef = useRef(null);
  const typingIntervalRef = useRef(null);
  const botReplyAddedRef = useRef(false);
  const messageInputRef = useRef(null);
  const isScrolledUpRef = useRef(false);

  useEffect(() => {
    if (messageInputRef.current) messageInputRef.current.focus();
  }, []);

  useEffect(() => {
    localStorage.setItem("darkMode", JSON.stringify(darkMode));
    document.body.className = darkMode ? "dark" : "light";
  }, [darkMode]);

  useEffect(() => { localStorage.setItem("chatLog", JSON.stringify(chatLog)); }, [chatLog]);
  useEffect(() => { localStorage.setItem("selectedModel", selectedModel); }, [selectedModel]);

  useEffect(() => {
    const chatBox = chatBoxRef.current;
    if (chatBox) {
      const atBottom = chatBox.scrollHeight - chatBox.scrollTop - chatBox.clientHeight < 100;
      if (!isScrolledUpRef.current || atBottom) {
        chatBox.scrollTop = chatBox.scrollHeight;
      }
    }
  }, [chatLog, loading, botTypingText]);

  useEffect(() => {
    const chatBox = chatBoxRef.current;
    if (chatBox) {
      const handleScroll = () => {
        const atBottom = chatBox.scrollHeight - chatBox.scrollTop - chatBox.clientHeight < 100;
        isScrolledUpRef.current = !atBottom;
      };
      chatBox.addEventListener('scroll', handleScroll);
      return () => chatBox.removeEventListener('scroll', handleScroll);
    }
  }, []);

  const typeEffect = useCallback((fullText) => {
    return new Promise((resolve) => {
      const words = fullText.split(' ');
      let wordIndex = 0;
      setBotTypingText("");
      if (typingIntervalRef.current) clearInterval(typingIntervalRef.current);
      
      typingIntervalRef.current = setInterval(() => {
        if (!abortControllerRef.current || !abortControllerRef.current.signal.aborted) {
          setBotTypingText((prev) => {
            if (wordIndex < words.length) {
              const newText = prev + (wordIndex > 0 ? ' ' : '') + words[wordIndex];
              wordIndex++;
              return newText;
            } else {
              clearInterval(typingIntervalRef.current);
              typingIntervalRef.current = null;
              if (!botReplyAddedRef.current) {
                setChatLog((prevLog) => [...prevLog, { sender: "bot", text: fullText, timestamp: new Date() }]);
                botReplyAddedRef.current = true;
              }
              setTimeout(() => {
                if (messageInputRef.current) messageInputRef.current.focus();
              }, 100);
              resolve();
              return prev;
            }
          });
        } else {
          clearInterval(typingIntervalRef.current);
          typingIntervalRef.current = null;
          resolve();
        }
      }, 50);
    });
  }, []);

  const stopTyping = useCallback(() => {
    if (typingIntervalRef.current) {
      clearInterval(typingIntervalRef.current);
      typingIntervalRef.current = null;
    }
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      abortControllerRef.current = null;
    }
    if (botTypingText.trim() !== "" && !botReplyAddedRef.current) {
      setChatLog((prev) => [...prev, { sender: "bot", text: botTypingText, timestamp: new Date() }]);
      botReplyAddedRef.current = true;
    }
    setLoading(false);
    setBotTypingText("");
    botReplyAddedRef.current = false;
  }, [botTypingText]);

  const sendMessage = useCallback(async () => {
    const messageToSend = message.trim();
    if (!messageToSend || loading) return;

    setChatLog((prev) => [...prev, { sender: "user", text: messageToSend, timestamp: new Date() }]);

    setLoading(true);
    setBotTypingText("");
    setMessage("");

    botReplyAddedRef.current = false;
    abortControllerRef.current = new AbortController();
    const signal = abortControllerRef.current.signal;

    try {
      const apiUrl = `/api/chat`;
      const messages = chatLog.map(msg => ({ sender: msg.sender, text: msg.text }));
      messages.push({ sender: 'user', text: messageToSend });

      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages, model: selectedModel }),
        signal,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(`API Error: ${response.status} - ${errorData.error || response.statusText}`);
      }

      const result = await response.json();
      let replyText = result.reply || "Sorry, couldn't get a response. Try again?";

      if (!signal.aborted) {
        await typeEffect(replyText);
      } else {
        setBotTypingText("");
      }
    } catch (error) {
      if (error.name !== "AbortError") {
        let errorMsg = `Connection issue: ${error.message || "Check your network and try again"}`;
        setChatLog((prev) => [...prev, { sender: "bot", text: errorMsg, timestamp: new Date() }]);
        setTimeout(() => {
          if (messageInputRef.current) messageInputRef.current.focus();
        }, 100);
      }
    } finally {
      if (!botReplyAddedRef.current && botTypingText.trim() !== "") {
        setChatLog((prev) => [...prev, { sender: "bot", text: botTypingText, timestamp: new Date() }]);
      }
      setLoading(false);
      setBotTypingText("");
      abortControllerRef.current = null;
      typingIntervalRef.current = null;
      botReplyAddedRef.current = false;
    }
  }, [message, loading, chatLog, typeEffect, botTypingText]);

  const handleNewChat = () => {
    if (window.confirm("Start a new chat? This will clear the current conversation.")) {
      setChatLog([]);
      setMessage("");
      setBotTypingText("");
      setLoading(false);
    }
  };

  return (
    <div className={`flex flex-col h-screen ${darkMode ? 'bg-[#212121] text-white' : 'bg-white text-gray-900'}`}>
      {/* Header */}
      <header className={`flex items-center justify-between px-4 py-3 border-b ${darkMode ? 'border-gray-700' : 'border-gray-200'}`}>
        <div className="flex items-center gap-3">
          <button
            onClick={handleNewChat}
            className={`px-4 py-2 rounded-lg text-sm font-medium ${
              darkMode ? 'bg-[#2f2f2f] hover:bg-[#3f3f3f]' : 'bg-gray-100 hover:bg-gray-200'
            }`}
          >
            New Chat
          </button>
          <h1 className="text-xl font-semibold">GPT Bro 😎</h1>
        </div>
        
        <div className="flex items-center gap-2">
          {/* Model Selector */}
          <div className="relative">
            <button
              onClick={() => setShowModelDropdown(!showModelDropdown)}
              className={`flex items-center gap-2 px-3 py-2 rounded-lg text-sm ${
                darkMode ? 'bg-[#2f2f2f] hover:bg-[#3f3f3f]' : 'bg-gray-100 hover:bg-gray-200'
              }`}
            >
              <span className="hidden sm:inline">{GEMINI_MODELS[selectedModel].name}</span>
              <span className="sm:hidden">Model</span>
              <ChevronDownIcon className={`h-4 w-4 transition-transform ${showModelDropdown ? 'rotate-180' : ''}`} />
            </button>
            
            {showModelDropdown && (
              <div className={`absolute right-0 mt-2 w-56 rounded-lg shadow-lg z-50 ${
                darkMode ? 'bg-[#2f2f2f] border border-gray-700' : 'bg-white border border-gray-200'
              }`}>
                {Object.entries(GEMINI_MODELS).map(([key, model]) => (
                  <button
                    key={key}
                    onClick={() => {
                      setSelectedModel(key);
                      setShowModelDropdown(false);
                    }}
                    className={`w-full text-left px-4 py-3 text-sm hover:bg-opacity-50 first:rounded-t-lg last:rounded-b-lg ${
                      darkMode ? 'hover:bg-gray-700' : 'hover:bg-gray-100'
                    } ${selectedModel === key ? 'font-semibold' : ''}`}
                  >
                    <div className="font-medium">{model.name}</div>
                    <div className={`text-xs ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>
                      {model.description}
                    </div>
                  </button>
                ))}
              </div>
            )}
          </div>
          
          {/* Dark Mode Toggle */}
          <button
            onClick={() => setDarkMode(!darkMode)}
            className={`p-2 rounded-lg ${darkMode ? 'hover:bg-[#2f2f2f]' : 'hover:bg-gray-100'}`}
          >
            {darkMode ? <SunIcon className="h-5 w-5" /> : <MoonIcon className="h-5 w-5" />}
          </button>
        </div>
      </header>

      {/* Chat Area */}
      <div ref={chatBoxRef} className="flex-1 overflow-y-auto px-4 py-6">
        <div className="max-w-3xl mx-auto space-y-6">
          {chatLog.length === 0 && !loading && (
            <div className="text-center py-20 text-gray-500">
              <div className="text-4xl mb-4">😎</div>
              <p className="text-lg">Start chatting with GPT Bro!</p>
              {userMemory.name && <p className="mt-2">Welcome back, {userMemory.name}!</p>}
            </div>
          )}
          
          {chatLog.map((msg, index) => (
            <div key={index} className={`flex gap-3 ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
              {msg.sender === 'bot' && (
                <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${darkMode ? 'bg-[#2f2f2f]' : 'bg-gray-200'}`}>
                  <SparklesIcon className="h-5 w-5" />
                </div>
              )}
              
              <div className={`max-w-[70%] ${msg.sender === 'user' ? 'order-first' : ''}`}>
                <div className={`rounded-2xl px-4 py-3 ${
                  msg.sender === 'user' 
                    ? darkMode ? 'bg-[#2f2f2f]' : 'bg-gray-100'
                    : ''
                }`}>
                  <div dangerouslySetInnerHTML={{ __html: formatMarkdown(msg.text) }} />
                </div>
              </div>
              
              {msg.sender === 'user' && (
                <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${darkMode ? 'bg-[#2f2f2f]' : 'bg-gray-200'}`}>
                  <UserIcon className="h-5 w-5" />
                </div>
              )}
            </div>
          ))}

          {loading && botTypingText && (
            <div className="flex gap-3">
              <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${darkMode ? 'bg-[#2f2f2f]' : 'bg-gray-200'}`}>
                <SparklesIcon className="h-5 w-5" />
              </div>
              <div className="max-w-[70%]">
                <div dangerouslySetInnerHTML={{ __html: formatMarkdown(botTypingText) }} />
                <span className="inline-block w-1 h-4 bg-gray-400 animate-pulse ml-1"></span>
              </div>
            </div>
          )}

          {loading && !botTypingText && (
            <div className="flex gap-3">
              <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${darkMode ? 'bg-[#2f2f2f]' : 'bg-gray-200'}`}>
                <SparklesIcon className="h-5 w-5 animate-pulse" />
              </div>
              <div className="flex items-center gap-1 text-gray-400">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce animation-delay-100"></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce animation-delay-200"></div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Input Area */}
      <div className={`border-t px-4 py-4 ${darkMode ? 'border-gray-700 bg-[#212121]' : 'border-gray-200 bg-white'}`}>
        <div className="max-w-3xl mx-auto">
          <div className={`flex items-center gap-2 rounded-3xl border ${darkMode ? 'border-gray-600 bg-[#2f2f2f]' : 'border-gray-300 bg-white'} px-4 py-2`}>
            <input
              ref={messageInputRef}
              type="text"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !loading && message.trim()) {
                  sendMessage();
                }
              }}
              placeholder="Message GPT Bro..."
              disabled={loading}
              className={`flex-1 bg-transparent border-none outline-none ${darkMode ? 'text-white placeholder-gray-500' : 'text-gray-900 placeholder-gray-400'}`}
            />
            
            <button
              onClick={loading ? stopTyping : sendMessage}
              disabled={(!message.trim() && !loading)}
              className={`p-2 rounded-full transition-colors ${
                loading 
                  ? 'bg-red-500 hover:bg-red-600 text-white' 
                  : message.trim()
                    ? darkMode 
                      ? 'bg-white hover:bg-gray-200 text-black'
                      : 'bg-black hover:bg-gray-800 text-white'
                    : 'bg-gray-300 cursor-not-allowed'
              }`}
            >
              {loading ? <StopIcon className="h-5 w-5" /> : <PaperAirplaneIcon className="h-5 w-5" />}
            </button>
          </div>
          <p className="text-xs text-center mt-2 text-gray-500">
            GPT Bro can make mistakes. Check important info.
          </p>
        </div>
      </div>

      <style>{`
        .animation-delay-100 { animation-delay: 0.1s; }
        .animation-delay-200 { animation-delay: 0.2s; }
        strong { font-weight: 600; }
        em { font-style: italic; }
        
        /* Scrollbar styles */
        ::-webkit-scrollbar {
          width: 8px;
        }
        ::-webkit-scrollbar-track {
          background: transparent;
        }
        ::-webkit-scrollbar-thumb {
          background: ${darkMode ? '#4a4a4a' : '#d1d5db'};
          border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
          background: ${darkMode ? '#5a5a5a' : '#9ca3af'};
        }
      `}</style>
    </div>
  );
}

export default App;
