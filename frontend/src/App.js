import React, { useState, useRef, useEffect, useLayoutEffect, useCallback } from "react";
import { SunIcon, MoonIcon, PaperAirplaneIcon, StopIcon, SparklesIcon, UserIcon, ArrowDownIcon } from "@heroicons/react/24/solid";

// Focusing the input on a touch device pops the on-screen keyboard up over the reply
const isTouchDevice = () => window.matchMedia("(pointer: coarse)").matches;

// Animated Title Component
const AnimatedTitle = () => {
  const [currentText, setCurrentText] = useState("");
  const [showBro, setShowBro] = useState(false);
  const [animationComplete, setAnimationComplete] = useState(false);

  useEffect(() => {
    const sequence = [
      { text: "Yo Bro 😎", delay: 1800 },
      { text: "Whatsup Bro 👋", delay: 1900 },
      { text: "Am Here 🔥", delay: 1900 },
      { text: "Guess Who 🤔", delay: 1900 },
      { text: "GPT.", delay: 1200 },
      { text: "GPT..", delay: 900 },
      { text: "GPT...", delay: 800 },
      { text: "GPT", delay: 600 }
    ];
    let timeoutId;
    let currentIndex = 0;

    const animateSequence = () => {
      if (currentIndex < sequence.length) {
        setCurrentText(sequence[currentIndex].text);
        
        timeoutId = setTimeout(() => {
          currentIndex++;
          if (currentIndex === sequence.length) {
            // Show "bro" sliding in and combine with "gpt"
            setTimeout(() => {
              setShowBro(true);
              setTimeout(() => {
                setCurrentText("GPT Bro 😎");
                setAnimationComplete(true);
              }, 700);
            }, 300);
          } else {
            animateSequence();
          }
        }, sequence[currentIndex].delay);
      }
    };

    // Check if animation already happened in this session
    const hasAnimated = sessionStorage.getItem('titleAnimated');
    if (!hasAnimated) {
      setTimeout(() => {
        animateSequence();
      }, 500); // Small delay before starting
      sessionStorage.setItem('titleAnimated', 'true');
    } else {
      setCurrentText("GPT Bro 😎");
      setAnimationComplete(true);
    }

    return () => {
      if (timeoutId) clearTimeout(timeoutId);
    };
  }, []);

  if (animationComplete) {
    return <h1 className="text-xl font-semibold">GPT Bro 😎</h1>;
  }

  return (
    <div className="relative h-7 flex items-center overflow-hidden">
      <h1 className="text-xl font-semibold transition-all duration-300 ease-in-out">
        {currentText === "gpt" && !showBro ? (
          <>
            gpt
            <span className="animate-pulse">...</span>
          </>
        ) : currentText === "gpt" && showBro ? (
          <>
            gpt
            <span className="inline-block animate-slide-in-right ml-1">
              bro 😎
            </span>
          </>
        ) : (
          <span className="inline-block">{currentText}</span>
        )}
      </h1>
    </div>
  );
};

// Function to format markdown-style text
const formatMarkdown = (text) => {
  text = text.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
  text = text.replace(/\*(.+?)\*/g, '<em>$1</em>');
  return text;
};

function App() {
  const [message, setMessage] = useState("");
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
  const lastUserMsgRef = useRef(null);
  // "anchor": follow the reply until the question reaches the top, "bottom": stick to the end,
  // "off": the user scrolled away, so leave the view alone
  const followModeRef = useRef("bottom");
  const userScrollIntentRef = useRef(false);
  const [showScrollDown, setShowScrollDown] = useState(false);

  useEffect(() => {
    if (messageInputRef.current && !isTouchDevice()) messageInputRef.current.focus();
  }, []);

  useEffect(() => {
    localStorage.setItem("darkMode", JSON.stringify(darkMode));
    document.body.className = darkMode ? "dark" : "light";
  }, [darkMode]);

  useEffect(() => { localStorage.setItem("chatLog", JSON.stringify(chatLog)); }, [chatLog]);

  // Like ChatGPT: follow the reply down only until the question reaches the top of the
  // chat area, then stop so a long answer can be read from its start
  useLayoutEffect(() => {
    const chatBox = chatBoxRef.current;
    if (!chatBox) return;
    const mode = followModeRef.current;
    if (mode !== "off") {
      let target = chatBox.scrollHeight - chatBox.clientHeight;
      const anchor = lastUserMsgRef.current;
      if (mode === "anchor" && anchor) {
        const anchorTop = anchor.getBoundingClientRect().top - chatBox.getBoundingClientRect().top + chatBox.scrollTop;
        target = Math.min(target, anchorTop - 16);
      }
      if (target > chatBox.scrollTop) chatBox.scrollTop = target;
    }
    setShowScrollDown(chatBox.scrollHeight - chatBox.scrollTop - chatBox.clientHeight > 120);
  }, [chatLog, loading, botTypingText]);

  useEffect(() => {
    const chatBox = chatBoxRef.current;
    if (!chatBox) return;
    // Only scrolls the user started change the follow mode, not ones caused by layout changes
    const markUserScroll = () => { userScrollIntentRef.current = true; };
    const handleScroll = () => {
      const distance = chatBox.scrollHeight - chatBox.scrollTop - chatBox.clientHeight;
      setShowScrollDown(distance > 120);
      if (userScrollIntentRef.current) followModeRef.current = distance < 40 ? "bottom" : "off";
    };
    const intentEvents = ["wheel", "touchmove", "mousedown"];
    intentEvents.forEach((e) => chatBox.addEventListener(e, markUserScroll, { passive: true }));
    chatBox.addEventListener("scroll", handleScroll, { passive: true });
    return () => {
      intentEvents.forEach((e) => chatBox.removeEventListener(e, markUserScroll));
      chatBox.removeEventListener("scroll", handleScroll);
    };
  }, []);

  const scrollToBottom = () => {
    const chatBox = chatBoxRef.current;
    if (!chatBox) return;
    followModeRef.current = "bottom";
    userScrollIntentRef.current = false;
    chatBox.scrollTo({ top: chatBox.scrollHeight, behavior: "smooth" });
  };

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
                if (messageInputRef.current && !isTouchDevice()) messageInputRef.current.focus();
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

    followModeRef.current = "anchor";
    userScrollIntentRef.current = false;
    // Close the on-screen keyboard so the reply gets the whole screen
    if (isTouchDevice() && messageInputRef.current) messageInputRef.current.blur();

    setChatLog((prev) => [...prev, { sender: "user", text: messageToSend, timestamp: new Date() }]);

    setLoading(true);
    setBotTypingText("");
    setMessage("");

    botReplyAddedRef.current = false;
    abortControllerRef.current = new AbortController();
    const signal = abortControllerRef.current.signal;

    try {
      const backendUrl = process.env.REACT_APP_BACKEND_URL;
      const apiUrl = backendUrl ? `${backendUrl}/api/chat` : '/api/chat';
      const messages = chatLog.map(msg => ({ sender: msg.sender, text: msg.text }));
      messages.push({ sender: 'user', text: messageToSend });

      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages }),
        signal,
      });

      let result;
      const responseText = await response.text();
      
      try {
        result = JSON.parse(responseText);
      } catch (parseError) {
        console.error("Response parsing error:", parseError);
        console.error("Raw response:", responseText);
        throw new Error(`Server returned invalid response. This usually means the API is not properly deployed. Status: ${response.status}`);
      }

      if (!response.ok) {
        throw new Error(`API Error: ${response.status} - ${result.error || response.statusText}`);
      }

      let replyText = result.reply || "Sorry, couldn't get a response. Try again?";

      if (!signal.aborted) {
        await typeEffect(replyText);
      } else {
        setBotTypingText("");
      }
    } catch (error) {
      if (error.name !== "AbortError") {
        let errorMsg;
        if (error.message.includes("invalid response") || error.message.includes("Unexpected token")) {
          errorMsg = "🔧 API deployment issue detected. The backend needs to be redeployed to fix the serverless function configuration.";
        } else {
          errorMsg = `Connection issue: ${error.message || "Check your network and try again"}`;
        }
        setChatLog((prev) => [...prev, { sender: "bot", text: errorMsg, timestamp: new Date() }]);
        setTimeout(() => {
          if (messageInputRef.current && !isTouchDevice()) messageInputRef.current.focus();
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

  const lastUserIndex = chatLog.map((msg) => msg.sender).lastIndexOf("user");

  const handleNewChat = () => {
    if (window.confirm("Start a new chat? This will clear the current conversation.")) {
      setChatLog([]);
      setMessage("");
      setBotTypingText("");
      setLoading(false);
    }
  };

  return (
    <div className={`flex flex-col h-full overflow-hidden ${darkMode ? 'bg-[#212121] text-white' : 'bg-white text-gray-900'}`}>
      {/* Header */}
      <header className={`flex-shrink-0 flex items-center justify-between px-4 py-3 border-b ${darkMode ? 'border-gray-700' : 'border-gray-200'}`}>
        <div className="flex items-center gap-3">
          <button
            onClick={handleNewChat}
            className={`px-4 py-2 rounded-lg text-sm font-medium ${
              darkMode ? 'bg-[#2f2f2f] hover:bg-[#3f3f3f]' : 'bg-gray-100 hover:bg-gray-200'
            }`}
          >
            New Chat
          </button>
          <AnimatedTitle />
        </div>
        
        <button
          onClick={() => setDarkMode(!darkMode)}
          className={`p-2 rounded-lg ${darkMode ? 'hover:bg-[#2f2f2f]' : 'hover:bg-gray-100'}`}
        >
          {darkMode ? <SunIcon className="h-5 w-5" /> : <MoonIcon className="h-5 w-5" />}
        </button>
      </header>

      {/* Chat Area */}
      <div ref={chatBoxRef} className="flex-1 overflow-y-auto px-4 py-6 min-h-0">
        <div className="max-w-3xl mx-auto space-y-6">
          {chatLog.length === 0 && !loading && (
            <div className="text-center py-20 text-gray-500">
              <div className="text-4xl mb-4">😎🔥</div>
              <p className="text-lg">Start chatting with GPT Bro! 💬</p>
              {userMemory.name && <p className="mt-2">Welcome back, {userMemory.name}! 👋</p>}
            </div>
          )}
          
          {chatLog.map((msg, index) => (
            <div key={index} ref={index === lastUserIndex ? lastUserMsgRef : null} className={`flex gap-3 ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
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
              {/* Same box as a finished reply, so the text doesn't shift when typing ends */}
              <div className="max-w-[70%]">
                <div className="rounded-2xl px-4 py-3">
                  <div dangerouslySetInnerHTML={{ __html: formatMarkdown(botTypingText) }} />
                  <span className="inline-block w-1 h-4 bg-gray-400 animate-pulse ml-1"></span>
                </div>
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
      <div className={`relative flex-shrink-0 border-t px-4 py-4 safe-area-inset-bottom ${darkMode ? 'border-gray-700 bg-[#212121]' : 'border-gray-200 bg-white'}`}>
        {showScrollDown && (
          <button
            onClick={scrollToBottom}
            aria-label="Scroll to latest message"
            className={`absolute -top-12 left-1/2 -translate-x-1/2 p-2 rounded-full border shadow-md ${
              darkMode ? 'bg-[#2f2f2f] border-gray-600 hover:bg-[#3f3f3f]' : 'bg-white border-gray-300 hover:bg-gray-100'
            }`}
          >
            <ArrowDownIcon className="h-4 w-4" />
          </button>
        )}
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
              placeholder="Message GPT Bro... 💬"
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
            GPT Bro can make mistakes. Check important info. ⚠️
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
