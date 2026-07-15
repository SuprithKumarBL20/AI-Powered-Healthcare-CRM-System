import React, { useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { editInteractionThunk, openConfirm, showToast } from '../store/slices.js';
import { 
  History, Calendar, ShieldCheck, AlertOctagon, Info, Edit, Trash, X, Save, AlertTriangle
} from 'lucide-react';

export default function HistoryPanel() {
  const dispatch = useDispatch();
  const { list: interactions, loading } = useSelector((state) => state.interaction);
  const { list: hcps } = useSelector((state) => state.hcp);

  // Edit states
  const [editingId, setEditingId] = useState(null);
  const [editDate, setEditDate] = useState('');
  const [editChannel, setEditChannel] = useState('');
  const [editSummary, setEditSummary] = useState('');
  const [editTopics, setEditTopics] = useState('');
  const [editTranscript, setEditTranscript] = useState('');
  const [editNextSteps, setEditNextSteps] = useState('');

  const handleStartEdit = (item) => {
    setEditingId(item.id);
    setEditDate(item.date);
    setEditChannel(item.channel);
    setEditSummary(item.summary || '');
    setEditTopics(item.discussion_topics || '');
    setEditTranscript(item.transcript || '');
    setEditNextSteps(item.next_steps || '');
  };

  const handleCancelEdit = () => {
    setEditingId(null);
  };

  const handleSaveEdit = async (id) => {
    try {
      const updates = {
        date: editDate,
        channel: editChannel,
        summary: editSummary,
        discussion_topics: editTopics,
        transcript: editTranscript,
        next_steps: editNextSteps
      };
      await dispatch(editInteractionThunk({ id, updates })).unwrap();
      setEditingId(null);
      dispatch(showToast('Interaction updated successfully (re-ran compliance engine)!', 'success'));
    } catch (e) {
      dispatch(showToast(`Failed to save edits: ${e}`, 'error'));
    }
  };

  const handleDelete = (id) => {
    dispatch(openConfirm({
      title: 'Delete Interaction Log',
      message: `Are you sure you want to delete interaction log #${id}? This action is permanent and cannot be undone.`,
      onConfirmType: 'delete_interaction',
      targetId: id
    }));
  };

  if (loading && interactions.length === 0) {
    return (
      <div className="history-panel loading-state">
        <div className="skeleton skeleton-line"></div>
        <div className="skeleton skeleton-line"></div>
      </div>
    );
  }

  return (
    <div className="history-section card">
      <div className="card-header">
        <div className="title-row">
          <History className="panel-icon text-secondary" />
          <h2 className="panel-title">Logged Interactions History</h2>
        </div>
        <p className="panel-subtitle">Review, audit compliance status, and edit records dynamically (uses Edit Interaction tool)</p>
      </div>

      <div className="history-list">
        {interactions.length === 0 ? (
          <div className="no-history-state">
            <Info size={24} className="no-history-icon" />
            <p>No historical interactions recorded. Log an interaction above to see history.</p>
          </div>
        ) : (
          interactions.map((item) => {
            const hcp = hcps.find((h) => h.id === item.hcp_id);
            const isEditing = editingId === item.id;
            
            const isCompliant = item.compliance_status === 'Compliant';
            const isNonCompliant = item.compliance_status === 'Non-Compliant';

            return (
              <div key={item.id} className={`history-card ${item.compliance_status?.toLowerCase()}`}>
                {isEditing ? (
                  /* EDIT MODE FOR AN INTERACTION */
                  <div className="edit-form-inner">
                    <div className="edit-header">
                      <h3>Editing Interaction #{item.id}</h3>
                      <button className="btn-icon" onClick={handleCancelEdit}>
                        <X size={16} />
                      </button>
                    </div>
                    
                    <div className="form-row">
                      <div className="form-group col-4">
                        <label>Date</label>
                        <input 
                          type="date" 
                          value={editDate} 
                          onChange={(e) => setEditDate(e.target.value)} 
                        />
                      </div>
                      <div className="form-group col-4">
                        <label>Channel</label>
                        <select 
                          value={editChannel} 
                          onChange={(e) => setEditChannel(e.target.value)}
                        >
                          <option value="In-Person">In-Person</option>
                          <option value="Video Call">Video Call</option>
                          <option value="Phone">Phone</option>
                          <option value="Email">Email</option>
                        </select>
                      </div>
                      <div className="form-group col-4">
                        <label>Discussion Topics</label>
                        <input 
                          type="text" 
                          value={editTopics} 
                          onChange={(e) => setEditTopics(e.target.value)} 
                        />
                      </div>
                    </div>

                    <div className="form-group">
                      <label>Interaction Summary</label>
                      <input 
                        type="text" 
                        value={editSummary} 
                        onChange={(e) => setEditSummary(e.target.value)} 
                      />
                    </div>

                    <div className="form-group">
                      <label>Transcript / Raw Notes (Updates compliance check dynamically!)</label>
                      <textarea 
                        rows={3}
                        value={editTranscript} 
                        onChange={(e) => setEditTranscript(e.target.value)} 
                      />
                    </div>

                    <div className="form-group">
                      <label>Next Steps</label>
                      <input 
                        type="text" 
                        value={editNextSteps} 
                        onChange={(e) => setEditNextSteps(e.target.value)} 
                      />
                    </div>

                    <div className="edit-actions">
                      <button className="btn btn-secondary btn-sm" onClick={handleCancelEdit}>
                        Cancel
                      </button>
                      <button className="btn btn-primary btn-sm" onClick={() => handleSaveEdit(item.id)}>
                        <Save size={12} className="btn-icon" />
                        Save Changes
                      </button>
                    </div>
                  </div>
                ) : (
                  /* VIEW MODE FOR AN INTERACTION */
                  <div className="history-card-inner">
                    <div className="card-top-row">
                      <div className="hcp-info">
                        <strong className="hcp-name">{hcp ? hcp.name : 'Unknown HCP'}</strong>
                        <span className="hcp-specialty-mini">{hcp ? hcp.specialty : ''}</span>
                      </div>
                      <div className="meta-badges">
                        <span className={`compliance-tag ${item.compliance_status?.toLowerCase()}`}>
                          {item.compliance_status === 'Compliant' ? (
                            <ShieldCheck size={12} className="icon-mr" />
                          ) : (
                            <AlertOctagon size={12} className="icon-mr" />
                          )}
                          {item.compliance_status}
                        </span>
                        <span className="date-tag">
                          <Calendar size={12} className="icon-mr" />
                          {item.date}
                        </span>
                      </div>
                    </div>

                    <div className="card-summary-block">
                      <p className="summary-text">{item.summary}</p>
                    </div>

                    {item.discussion_topics && (
                      <div className="topics-row">
                        <strong>Discussed:</strong>
                        {item.discussion_topics.split(',').map((topic, i) => (
                          <span key={i} className="chip-mini">{topic.trim()}</span>
                        ))}
                      </div>
                    )}

                    {item.compliance_notes && !isCompliant && (
                      <div className="compliance-warning-note">
                        <AlertTriangle size={14} className="warning-icon" />
                        <div>
                          <strong>Compliance Flag:</strong>
                          <p>{item.compliance_notes}</p>
                        </div>
                      </div>
                    )}

                    {item.compliance_flags && item.compliance_flags.length > 0 && (
                      <div className="compliance-flags-container">
                        {item.compliance_flags.map((flag) => (
                          <div key={flag.id} className="flag-details-item">
                            <span className="rule-name">{flag.rule_matched} ({flag.severity} Severity)</span>
                            <p className="rule-desc">{flag.description}</p>
                          </div>
                        ))}
                      </div>
                    )}

                    {item.next_steps && (
                      <div className="next-steps-block">
                        <strong>Action Item:</strong> <span>{item.next_steps}</span>
                        {item.follow_up_date && (
                          <span className="due-badge">Due {item.follow_up_date}</span>
                        )}
                      </div>
                    )}

                    <div className="card-actions">
                      <button className="btn-action-icon text-primary" onClick={() => handleStartEdit(item)}>
                        <Edit size={14} />
                        <span>Edit</span>
                      </button>
                      <button className="btn-action-icon text-danger" onClick={() => handleDelete(item.id)}>
                        <Trash size={14} />
                        <span>Delete</span>
                      </button>
                    </div>
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
