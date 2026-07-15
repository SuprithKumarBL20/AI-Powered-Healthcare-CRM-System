import React, { useState, useRef, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { sendMessageToAgent, addMessage, clearChat, fetchInteractions, fetchHcps, showToast } from '../store/slices.js';
import { 
  Send, Sparkles, AlertCircle, RefreshCw, Trash2, FileText, 
  CheckCircle, FileSearch, HelpCircle, Shield, Award 
} from 'lucide-react';

export default function ChatInterface() {
  const dispatch = useDispatch();
  const { messages, extractedState, complianceCheck, recommendations, loading } = useSelector((state) => state.chat);
  const { list: hcps, selectedHcpId } = useSelector((state) => state.hcp);
  
  const [inputText, setInputText] = useState('');
  const chatEndRef = useRef(null);

  const activeHcp = hcps.find(h => h.id === selectedHcpId);

  useEffect(() => {
    // Scroll chat to bottom
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!inputText.trim()) return;
    if (!selectedHcpId) {
      dispatch(showToast('Please select an HCP on the left panel first.', 'warning'));
      return;
    }

    const userMsg = {
      role: 'user',
      content: inputText
    };

    dispatch(addMessage(userMsg));
    setInputText('');

    try {
      // Gather conversation history
      const history = [...messages, userMsg];
      const result = await dispatch(sendMessageToAgent({ messages: history, hcpId: selectedHcpId })).unwrap();
      
      // If a tool logged an interaction or updated next steps, refresh list
      if (result.extracted_state && result.extracted_state.logged_id) {
        dispatch(fetchInteractions());
        dispatch(fetchHcps());
      }
    } catch (e) {
      console.error("Agent chat failed: ", e);
    }
  };

  const handleClear = () => {
    dispatch(clearChat());
  };

  // Helper to suggest a prompt click
  const handleQuickPrompt = (text) => {
    if (activeHcp) {
      const formatted = text.replace('{HCP}', activeHcp.name);
      setInputText(formatted);
    }
  };

  return (
    <div className="chat-container">
      {/* Main Chat Area */}
      <div className="chat-main card">
        <div className="card-header chat-header">
          <div className="header-meta">
            <Sparkles className="header-icon text-primary animate-pulse" />
            <h2 className="panel-title">Conversational AI Logger</h2>
          </div>
          <button className="btn-icon-text btn-clear" onClick={handleClear}>
            <Trash2 size={14} />
            Clear Chat
          </button>
        </div>

        <div className="chat-messages">
          {messages.map((msg, idx) => {
            const isAI = msg.role === 'assistant';
            return (
              <div key={idx} className={`message-bubble-wrapper ${isAI ? 'ai' : 'user'}`}>
                <div className="message-avatar">
                  {isAI ? <Sparkles size={14} /> : <FileText size={14} />}
                </div>
                <div className="message-bubble">
                  <p className="message-content">{msg.content}</p>
                </div>
              </div>
            );
          })}
          {loading && (
            <div className="message-bubble-wrapper ai">
              <div className="message-avatar">
                <RefreshCw size={14} className="spin" />
              </div>
              <div className="message-bubble loading-bubble">
                <span className="dot"></span>
                <span className="dot"></span>
                <span className="dot"></span>
              </div>
            </div>
          )}
          <div ref={chatEndRef} />
        </div>

        <div className="quick-prompts">
          <span className="quick-prompt-label">Try saying:</span>
          {activeHcp && (
            <>
              <button 
                className="chip chip-action" 
                onClick={() => handleQuickPrompt(`Log an in-person meeting with {HCP} today. We discussed Zyntra efficacy. Sentiment was very positive. Next step: email the cardiovascular safety overview on 2026-07-20.`)}
              >
                "Log Zyntra meeting today..."
              </button>
              <button 
                className="chip chip-action" 
                onClick={() => handleQuickPrompt(`Check compliance for: I promised to sponsor travel and hotel tickets to Hawaii for {HCP} to attend the next summit.`)}
              >
                "Check Hawaii travel compliance..."
              </button>
              <button 
                className="chip chip-action" 
                onClick={() => handleQuickPrompt(`Show profile details for {HCP}`)}
              >
                "Show profile details..."
              </button>
            </>
          )}
        </div>

        <form onSubmit={handleSend} className="chat-input-row">
          <input
            type="text"
            className="chat-input"
            placeholder={activeHcp ? `Type instructions regarding ${activeHcp.name}...` : "Select an HCP on left to begin..."}
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            disabled={loading || !selectedHcpId}
          />
          <button 
            type="submit" 
            className="btn btn-primary btn-chat-send"
            disabled={loading || !inputText.trim() || !selectedHcpId}
          >
            <Send size={16} />
          </button>
        </form>
      </div>

      {/* Real-time Extracted Field Panel */}
      <div className="chat-sidebar">
        {/* Sync panel */}
        <div className="sync-panel card">
          <div className="card-header">
            <h3 className="card-title-sm">Live Extraction State</h3>
            <span className="status-badge pulse-success">Synced</span>
          </div>
          <div className="card-body">
            {extractedState ? (
              <div className="extracted-fields-list">
                <div className="extracted-item">
                  <span className="extracted-label">Log ID:</span>
                  <span className="extracted-value badge-success">#{extractedState.logged_id || 'Draft'}</span>
                </div>
                <div className="extracted-item">
                  <span className="extracted-label">Date:</span>
                  <span className="extracted-value">{extractedState.date || 'N/A'}</span>
                </div>
                <div className="extracted-item">
                  <span className="extracted-label">Channel:</span>
                  <span className="extracted-value">{extractedState.channel || 'N/A'}</span>
                </div>
                <div className="extracted-item">
                  <span className="extracted-label">Topics:</span>
                  <span className="extracted-value font-semibold text-primary">{extractedState.discussion_topics || 'N/A'}</span>
                </div>
                <div className="extracted-item">
                  <span className="extracted-label">Sentiment:</span>
                  <span className="extracted-value">{extractedState.sentiment || 'N/A'}</span>
                </div>
                <div className="extracted-item">
                  <span className="extracted-label">Compliance:</span>
                  <span className={`extracted-value badge-${extractedState.compliance_status?.toLowerCase() === 'compliant' ? 'success' : 'danger'}`}>
                    {extractedState.compliance_status || 'N/A'}
                  </span>
                </div>
                {extractedState.compliance_notes && (
                  <div className="extracted-block compliance-notes-block">
                    <strong>Compliance Notes:</strong>
                    <p>{extractedState.compliance_notes}</p>
                  </div>
                )}
                <div className="extracted-block">
                  <strong>AI Summary:</strong>
                  <p>{extractedState.summary || 'N/A'}</p>
                </div>
                <div className="extracted-block">
                  <strong>Next Best Action:</strong>
                  <p className="text-secondary italic">{extractedState.next_steps || 'N/A'}</p>
                </div>
              </div>
            ) : (
              <div className="empty-state">
                <FileSearch size={32} className="empty-icon" />
                <p>No logged interaction drafts yet. Send a message to the AI agent to log interaction or fetch profiles, and extracted fields will populate here in real-time.</p>
              </div>
            )}
          </div>
        </div>

        {/* Compliance checklist */}
        {complianceCheck && (
          <div className="compliance-eval-panel card">
            <div className="card-header">
              <h3 className="card-title-sm">Compliance Engine Analysis</h3>
            </div>
            <div className="card-body">
              <div className={`comp-status-header ${complianceCheck.compliance_status.toLowerCase()}`}>
                <Shield size={14} />
                <span>{complianceCheck.compliance_status}</span>
              </div>
              <p className="comp-rec-text">{complianceCheck.recommendation}</p>
              
              {complianceCheck.flags && complianceCheck.flags.length > 0 && (
                <div className="comp-flags-list">
                  {complianceCheck.flags.map((flag, i) => (
                    <div key={i} className="comp-flag-card">
                      <span className="flag-title">{flag.rule}</span>
                      <p className="flag-details">{flag.description}</p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
