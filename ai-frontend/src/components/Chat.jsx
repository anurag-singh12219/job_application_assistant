import { useState, useRef, useEffect } from "react";
import { getCareerAdvice, getCareerAdviceWithFile } from "../api/backend";
import "./Chat.css";

export default function Chat({ chatHistory, setChatHistory }) {
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [isSending, setIsSending] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);
  const fileInputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [chatHistory, loading]);

  // Listen to custom newChat event from navigation/sidebar
  useEffect(() => {
    const handleNewChatEvent = () => {
      setChatHistory([]);
      setUploadedFiles([]);
      setInput("");
    };
    window.addEventListener("newChat", handleNewChatEvent);
    return () => window.removeEventListener("newChat", handleNewChatEvent);
  }, [setChatHistory]);

  // Handle multiple file uploads
  const handleFileUpload = (e) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      const newFiles = Array.from(files).map((file) => ({
        file,
        name: file.name,
        id: Date.now() + Math.random()
      }));
      setUploadedFiles((prev) => [...prev, ...newFiles]);
    }
    e.target.value = "";
  };

  // Remove a specific file from the list
  const removeFile = (fileId) => {
    setUploadedFiles((prev) => prev.filter((f) => f.id !== fileId));
  };

  const handleSend = async (text = null) => {
    const typed = text || input.trim();
    const message = typed || (uploadedFiles.length > 0 ? "Please analyze the uploaded files and provide career advice." : "");
    if (!message && uploadedFiles.length === 0) return;

    // Add user message with file references
    const userMessage = { 
      role: "user", 
      content: message,
      fileNames: uploadedFiles.map((f) => f.name) || [],
      timestamp: new Date() 
    };
    const newHistory = [...chatHistory, userMessage];
    setChatHistory(newHistory);
    setInput("");
    setIsSending(true);
    setLoading(true);

    try {
      let response;
      if (uploadedFiles.length > 0) {
        const formData = new FormData();
        formData.append("file", uploadedFiles[0].file);
        formData.append("query", message);
        
        uploadedFiles.slice(1).forEach((fileObj, idx) => {
          formData.append(`additional_file_${idx}`, fileObj.file);
        });
        
        response = await getCareerAdviceWithFile(formData);
      } else {
        response = await getCareerAdvice({ query: message });
      }
      
      const aiResponse = {
        role: "assistant",
        content: response.advice || response.response || getDefaultResponse(message),
        fileNames: uploadedFiles.map((f) => f.name),
        timestamp: new Date()
      };
      setChatHistory((prev) => [...prev, aiResponse]);
      setUploadedFiles([]);
    } catch (error) {
      console.error("Chat error:", error);
      const fallbackResponse = {
        role: "assistant",
        content: getDefaultResponse(message),
        fileNames: uploadedFiles.map((f) => f.name),
        timestamp: new Date()
      };
      setChatHistory((prev) => [...prev, fallbackResponse]);
    } finally {
      setIsSending(false);
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const getDefaultResponse = (query) => {
    const lowerQuery = query.toLowerCase();
    
    if (lowerQuery.includes("resume") || lowerQuery.includes("cv")) {
      return "Great question about resumes! Here are my top recommendations:\n\n✅ **Key Resume Tips:**\n• Tailor it for each position - match keywords from the job description\n• Use action verbs (Led, Developed, Increased, Optimized)\n• Quantify your achievements with numbers and percentages\n• Keep formatting clean and scannable - use bullet points\n• Aim for 1-2 pages; 3 pages max for 10+ years experience\n• Include relevant skills section highlighting technical competencies\n• Use power words that match the job description\n\n📊 **ATS Optimization:**\n• Use standard fonts and formatting\n• Include relevant keywords without keyword stuffing\n• Avoid tables, images, and complex graphics\n• Save as PDF to preserve formatting\n\nWould you like me to analyze your resume? Upload it in the Resume Analysis section!";
    } else if (lowerQuery.includes("interview")) {
      return "Excellent - interview prep is crucial! Here's my comprehensive guide:\n\n🎯 **Before the Interview:**\n• Research the company thoroughly - mission, values, recent news\n• Study the job description and prepare examples\n• Prepare 3-5 questions to ask the interviewer\n• Test your tech setup if it's a video interview\n• Prepare copies of your resume\n\n⭐ **During the Interview - STAR Method:**\nStructure your answers:\n• **Situation** - Set the context\n• **Task** - Describe your responsibility\n• **Action** - Explain what you did\n• **Result** - Share the positive outcome with metrics\n\n💡 **Top Questions to Prepare:**\n• Tell me about yourself\n• Why do you want this role?\n• What's your greatest strength/weakness?\n• Describe your experience with [key skill]\n• How do you handle conflict/pressure?\n\nUse our Interview Prep tool for 25+ AI-generated practice questions!";
    } else if (lowerQuery.includes("salary") || lowerQuery.includes("negotiate")) {
      return "Smart salary negotiation is a crucial skill! Here's my detailed strategy:\n\n💰 **Research Phase:**\n• Check Glassdoor, LinkedIn Salary, Payscale, Levels.fyi\n• Consider location, company size, and your experience\n• Build a range: minimum, target, and ideal salary\n• Factor in total compensation (bonuses, stock, benefits)\n\n🤝 **Negotiation Strategy:**\n• Let them make the first offer\n• Don't share your previous salary\n• Use collaborative language (\"I'm excited about this, and...\") \n• Build your case with market data\n• Consider non-monetary benefits (remote work, flexibility, growth)\n• Get the offer in writing\n\n📈 **Leverage Points:**\n• Your specific skills and experience\n• Market rates for your role\n• Your track record of results\n• Additional responsibilities you'll take on\n\nUse our Salary Negotiation tool for personalized insights!";
    } else if (lowerQuery.includes("cover letter")) {
      return "Creating engaging cover letters is an art and science! Here's how to shine:\n\n✍️ **Structure:**\n• **Header** - Your contact info and date\n• **Opening** - Hook them immediately (why this company matters to you)\n• **Body** - 2-3 paragraphs connecting your experience to their needs\n• **Closing** - Call to action and thank you\n\n🌟 **Writing Tips:**\n• Personalize it for each company (use their name, products, news)\n• Show enthusiasm and genuine interest\n• Use the same keywords from the job posting\n• Tell a story - don't just repeat your resume\n• Keep it to 250-400 words\n• Use a professional tone but show your personality\n• Proofread 3 times!\n\n✅ **What Hiring Managers Want:**\n• Why you specifically want this role\n• How your experience solves their problems\n• Examples of your impact\n• Understanding of their company/industry\n\nGenerate personalized cover letters instantly with our AI tool!";
    } else if (lowerQuery.includes("job search") || lowerQuery.includes("find job")) {
      return "Finding the right job requires strategy! Here's my playbook:\n\n🔍 **Job Search Strategy:**\n• Use multiple platforms: LinkedIn, Indeed, company websites\n• Set up job alerts for your target roles\n• Follow companies you're interested in\n• Join relevant communities and forums\n• Customize each application\n• Track your applications\n\n🤝 **Networking (most effective!):**\n• 70% of jobs are found through networking\n• Reach out to contacts on LinkedIn\n• Attend industry meetups and conferences\n• Informational interviews with professionals\n• Engage with LinkedIn posts in your field\n• Join online communities in your niche\n\n📝 **Application Tips:**\n• Customize cover letter and resume for each role\n• Highlight keywords from job description\n• Show enthusiasm and specific interest\n• Follow application instructions exactly\n• Include portfolio links if applicable\n\n⏰ **Follow Up:**\n• Wait 5-7 business days before following up\n• Keep it polite and brief\n• Reference the specific position\n• Reiterate your interest\n\nExplore our Job Search feature to discover opportunities!";
    } else if (lowerQuery.includes("skill") || lowerQuery.includes("learn")) {
      return "Great initiative on skill development! Here's a learning roadmap:\n\n📚 **Best Learning Resources:**\n• **Free**: Coursera Audit, YouTube, freeCodeCamp, Udemy free courses\n• **Paid**: Coursera, Udemy, Pluralsight, Codecademy, Skillshare\n• **Practice**: LeetCode, HackerRank, GitHub projects\n• **Earn Certs**: Google Career Certificates, AWS certifications\n\n🎯 **Learning Strategy:**\n• Focus on 1-2 skills at a time\n• Combine theory with practice projects\n• Build real projects for your portfolio\n• Share your projects on GitHub\n• Join communities (Reddit, Discord, Slack)\n• Complete practice challenges\n\n📈 **Building Your Portfolio:**\n• Create 3-5 portfolio projects\n• Show your growth over time\n• Include links in your resume\n• Document your process\n• Contributed to open source\n\n⏱️ **Learning Timeline:**\n• Beginner to intermediate: 3-6 months\n• Intermediate to advanced: 6-12 months\n• Consistency beats intensity\n\nWhat skill are you looking to develop?";
    } else {
      return "👋 **Welcome to Your AI Career Assistant!**\n\nI'm here to help you with:\n\n📄 **Resumes** - Tips, optimization, ATS strategies\n💬 **Interviews** - Prep, questions, STAR method\n💰 **Salary** - Negotiation, market research, offers\n✍️ **Cover Letters** - Writing tips and best practices\n🎯 **Job Search** - Strategies, networking, applications\n🎓 **Skills** - Learning paths and development\n\n**Or ask me anything about:**\n• Career transitions\n• Freelancing/consulting\n• Remote work\n• Career growth\n• Professional development\n\n📌 **Pro Tips:**\n• Use our specialized tools for detailed analysis\n• Combine practical advice with actionable tools\n• Your journey is unique - customize advice to your situation\n\nWhat's your biggest career challenge right now?";
    }
  };

  const suggestedQuestions = [
    "How can I improve my resume for tech roles?",
    "What's the STAR method for interviews?",
    "How do I negotiate a better salary?",
    "What skills should I learn this year?"
  ];

  return (
    <div className="chat-container">
      {/* Chat Sub-header */}
      <div className="chat-header-modern">
        <div className="chat-header-row">
          <div className="chat-title-group">
            <h1>🤖 AI Career Copilot</h1>
            <p>24/7 personalized guidance on resumes, interview prep, salary negotiation, and career growth</p>
          </div>
          <button
            className="chat-header-upload-btn"
            onClick={() => fileInputRef.current?.click()}
            title="Upload resume or document for AI context"
          >
            <span>📎 Upload File</span>
          </button>
        </div>
      </div>

      {/* Chat Messages Stream */}
      <div className="chat-messages">
        {chatHistory.length === 0 && (
          <div className="chat-empty">
            <div className="chat-empty-icon">💼</div>
            <h3>Welcome to Your AI Career Assistant</h3>
            <p>Ask anything about your job hunt, interview strategies, or upload your resume for tailored feedback.</p>
            <div className="suggested-section">
              <p className="suggested-title">Quick prompts to get started:</p>
              <div className="suggested-questions">
                {suggestedQuestions.map((q, idx) => (
                  <button 
                    key={idx}
                    onClick={() => handleSend(q)} 
                    className="suggested-btn"
                  >
                    <span>{q}</span>
                    <span className="suggested-arrow">→</span>
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}

        {chatHistory.map((msg, idx) => (
          <div key={idx} className={`message message-${msg.role}`}>
            <div className="message-avatar">
              {msg.role === "user" ? "👤" : "🤖"}
            </div>
            <div className="message-content">
              {msg.fileNames && msg.fileNames.length > 0 && (
                <div className="message-files">
                  {msg.fileNames.map((fn, i) => (
                    <span key={i} className="message-file-badge">📎 {fn}</span>
                  ))}
                </div>
              )}
              <div className="message-text">
                {msg.content.split("\n").map((line, i) => (
                  line.trim() && <p key={i}>{line}</p>
                ))}
              </div>
              <span className="message-time">
                {msg.timestamp?.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
              </span>
            </div>
          </div>
        ))}

        {loading && (
          <div className="message message-assistant">
            <div className="message-avatar">🤖</div>
            <div className="message-content">
              <div className="typing-indicator">
                <span />
                <span />
                <span />
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Chat Input Dock */}
      <div className="chat-input-area">
        {uploadedFiles.length > 0 && (
          <div className="files-list">
            <div className="files-label">Attached ({uploadedFiles.length}):</div>
            <div className="files-container">
              {uploadedFiles.map((fileObj) => (
                <div key={fileObj.id} className="file-item">
                  <span className="file-name">📄 {fileObj.name}</span>
                  <button 
                    className="file-remove"
                    onClick={() => removeFile(fileObj.id)}
                    title="Remove file"
                  >
                    ✕
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}

        <div className="input-controls">
          <button
            className="file-upload-btn"
            onClick={() => fileInputRef.current?.click()}
            title="Upload documents for AI context"
            type="button"
          >
            <span>📎</span>
            <span className="upload-btn-text">Attach</span>
          </button>
          <input
            ref={fileInputRef}
            type="file"
            hidden
            onChange={handleFileUpload}
            accept=".pdf,.txt,.doc,.docx"
            multiple
          />
          <textarea
            ref={inputRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyPress}
            placeholder="Ask me anything about careers, resumes, interviews... (Shift+Enter for new line)"
            disabled={isSending}
            className="chat-input"
            rows="2"
          />
          <button 
            onClick={() => handleSend()} 
            disabled={(!input.trim() && uploadedFiles.length === 0) || isSending}
            className={`send-btn ${isSending ? "sending" : ""}`}
            type="button"
          >
            {isSending ? (
              <>
                <span className="chat-spinner" />
                <span>Thinking...</span>
              </>
            ) : (
              <>
                <span>Send</span>
                <span className="send-arrow">↑</span>
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
}
