import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useSelector, useDispatch } from 'react-redux';
import { fetchHcps, openConfirm, openEmail, showToast } from '../store/slices.js';
import { Mail, CheckSquare, Clock, Edit3, Send, RefreshCw, ChevronDown, ChevronUp } from 'lucide-react';

export default function FollowUpPanel() {
  const dispatch = useDispatch();
  const { list: hcps } = useSelector((state) => state.hcp);
  const [followUps, setFollowUps] = useState([]);
  const [loading, setLoading] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [editedEmail, setEditedEmail] = useState('');
  const [expandedId, setExpandedId] = useState(null);

  const fetchFollowUps = async () => {
    setLoading(true);
    try {
      const res = await axios.get('/api/follow-ups');
      setFollowUps(res.data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchFollowUps();
  }, [hcps]); // Refresh when HCP list changes (due to new logging)

  const handleToggleExpand = (id, email) => {
    if (expandedId === id) {
      setExpandedId(null);
      setEditingId(null);
    } else {
      setExpandedId(id);
      setEditedEmail(email || '');
      setEditingId(null);
    }
  };

  const handleUpdateStatus = (id, newStatus) => {
    if (newStatus === 'Completed') {
      dispatch(openConfirm({
        title: 'Complete Follow-Up Task',
        message: 'Are you sure you want to mark this follow-up task as Completed?',
        onConfirmType: 'complete_task',
        targetId: id
      }));
    }
  };

  const handleSaveEmail = async (id) => {
    try {
      await axios.put(`/api/follow-ups/${id}`, { recommended_email: editedEmail });
      fetchFollowUps();
      setEditingId(null);
      dispatch(showToast('Email draft updated successfully!', 'success'));
    } catch (e) {
      dispatch(showToast('Error updating email draft.', 'error'));
    }
  };

  const handleSendMockEmail = (email) => {
    dispatch(openEmail({
      title: 'Mock SMTP Dispatch Triggered!',
      emailContent: email
    }));
  };

  return (
    <div className="followup-section card">
      <div className="card-header">
        <h2 className="panel-title">Follow-up Tasks & AI Email Drafts</h2>
        <p className="panel-subtitle">Manage scheduled follow-ups and dispatch customized communication scripts</p>
      </div>

      <div className="followup-list">
        {loading && followUps.length === 0 ? (
          <div className="loading-state">
            <RefreshCw size={24} className="spin text-primary" />
          </div>
        ) : followUps.length === 0 ? (
          <div className="empty-state">
            <Clock size={24} className="empty-icon text-secondary" />
            <p>No follow-ups currently scheduled.</p>
          </div>
        ) : (
          followUps.map((item) => {
            const hcp = hcps.find(h => h.id === item.hcp_id);
            const isExpanded = expandedId === item.id;
            const isEditing = editingId === item.id;

            return (
              <div key={item.id} className={`followup-card ${item.status.toLowerCase()}`}>
                <div className="followup-summary-row" onClick={() => handleToggleExpand(item.id, item.recommended_email)}>
                  <div className="followup-title-info">
                    <span className={`status-dot ${item.status.toLowerCase()}`}></span>
                    <div>
                      <strong className="followup-title">{item.title}</strong>
                      <div className="followup-meta">
                        <span>For: <strong>{hcp ? hcp.name : 'Unknown HCP'}</strong></span>
                        <span className="meta-separator">•</span>
                        <span>Due: {item.due_date || 'N/A'}</span>
                      </div>
                    </div>
                  </div>
                  
                  <div className="followup-action-buttons" onClick={(e) => e.stopPropagation()}>
                    {item.status === 'Pending' && (
                      <button 
                        className="btn btn-sm btn-outline-success"
                        onClick={() => handleUpdateStatus(item.id, 'Completed')}
                      >
                        <CheckSquare size={12} className="btn-icon" />
                        Complete
                      </button>
                    )}
                    <button className="btn-toggle-expand">
                      {isExpanded ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                    </button>
                  </div>
                </div>

                {isExpanded && (
                  <div className="followup-detail-drawer">
                    <p className="task-desc"><strong>Task Description:</strong> {item.description || 'No description provided.'}</p>
                    
                    {item.recommended_email && (
                      <div className="email-draft-box">
                        <div className="email-draft-header">
                          <div className="email-header-left">
                            <Mail size={14} className="email-icon text-primary" />
                            <span>AI Recommended Email Script</span>
                          </div>
                          
                          <div className="email-header-actions">
                            {!isEditing ? (
                              <button 
                                className="btn-text-sm"
                                onClick={() => setEditingId(item.id)}
                              >
                                <Edit3 size={12} />
                                Edit Draft
                              </button>
                            ) : (
                              <button 
                                className="btn-text-sm text-success"
                                onClick={() => handleSaveEmail(item.id)}
                              >
                                Save Changes
                              </button>
                            )}
                          </div>
                        </div>

                        {isEditing ? (
                          <textarea
                            className="email-textarea"
                            rows={8}
                            value={editedEmail}
                            onChange={(e) => setEditedEmail(e.target.value)}
                          />
                        ) : (
                          <pre className="email-preview">{item.recommended_email}</pre>
                        )}

                        <div className="email-action-row">
                          <button 
                            className="btn btn-primary btn-sm btn-send-email"
                            onClick={() => handleSendMockEmail(isEditing ? editedEmail : item.recommended_email)}
                          >
                            <Send size={12} className="btn-icon" />
                            Dispatch Email Draft
                          </button>
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}
