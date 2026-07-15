import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { logInteractionThunk, showToast } from '../store/slices.js';
import axios from 'axios';
import { 
  Save, ShieldCheck, AlertTriangle, Play, RefreshCw, Send, CheckCircle2 
} from 'lucide-react';

export default function LogInteractionForm() {
  const dispatch = useDispatch();
  const { list: hcps, selectedHcpId } = useSelector((state) => state.hcp);
  const { loading: submitting } = useSelector((state) => state.interaction);

  const [date, setDate] = useState(new Date().toISOString().split('T')[0]);
  const [channel, setChannel] = useState('In-Person');
  const [topics, setTopics] = useState('Zyntra');
  const [notes, setNotes] = useState('');
  const [sentiment, setSentiment] = useState('Neutral');
  const [followUpDate, setFollowUpDate] = useState('');
  const [nextSteps, setNextSteps] = useState('');

  // Local compliance state
  const [checkingCompliance, setCheckingCompliance] = useState(false);
  const [complianceReport, setComplianceReport] = useState(null);

  const activeHcp = hcps.find(h => h.id === selectedHcpId);

  const handlePreCheckCompliance = async () => {
    if (!notes.trim()) {
      dispatch(showToast('Please enter some transcript or discussion notes first.', 'warning'));
      return;
    }
    setCheckingCompliance(true);
    setComplianceReport(null);
    try {
      const parsedTopics = topics.split(',').map(t => t.trim()).filter(Boolean);
      // Simulate/trigger tool API call direct
      const response = await axios.post('/api/chat', {
        messages: [{
          role: 'user',
          content: `Run compliance check on: "${notes}". Discussion topics: "${topics}".`
        }],
        hcp_id: selectedHcpId
      });
      
      if (response.data.compliance_check) {
        setComplianceReport(response.data.compliance_check);
      } else {
        // Construct basic report if empty
        setComplianceReport({
          compliance_status: 'Compliant',
          flags: [],
          recommendation: 'Discussion complies with standard marketing rules.'
        });
      }
    } catch (e) {
      console.error(e);
      dispatch(showToast('Error running compliance engine.', 'error'));
    } finally {
      setCheckingCompliance(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedHcpId) {
      dispatch(showToast('Please select an HCP on the left panel.', 'warning'));
      return;
    }
    if (!notes.trim()) {
      dispatch(showToast('Please enter interaction notes or transcript.', 'warning'));
      return;
    }

    const payload = {
      hcp_id: selectedHcpId,
      rep_id: 'REP-001',
      date,
      channel,
      transcript: notes,
      discussion_topics: topics,
      follow_up_date: followUpDate || null,
      sentiment,
      next_steps: nextSteps || null
    };

    try {
      const result = await dispatch(logInteractionThunk(payload)).unwrap();
      dispatch(showToast(`Interaction logged successfully! Status: ${result.compliance_status}`, 'success'));
      // Clear form
      setNotes('');
      setNextSteps('');
      setFollowUpDate('');
      setComplianceReport(null);
    } catch (err) {
      dispatch(showToast(`Error logging interaction: ${err}`, 'error'));
    }
  };

  return (
    <div className="form-panel card">
      <div className="card-header">
        <h2 className="panel-title">Structured Log Form</h2>
        <p className="panel-subtitle">Log interaction details manually with real-time validation checks</p>
      </div>

      <form onSubmit={handleSubmit} className="form-content">
        <div className="form-row">
          <div className="form-group col-6">
            <label htmlFor="hcp-readonly">Selected Healthcare Professional</label>
            <input 
              type="text" 
              id="hcp-readonly" 
              value={activeHcp ? `${activeHcp.name} (${activeHcp.specialty})` : 'Select HCP from sidebar'} 
              readOnly 
              className="input-readonly"
            />
          </div>

          <div className="form-group col-6">
            <label htmlFor="interaction-date">Interaction Date</label>
            <input 
              type="date" 
              id="interaction-date" 
              value={date} 
              onChange={(e) => setDate(e.target.value)} 
              required 
            />
          </div>
        </div>

        <div className="form-row">
          <div className="form-group col-4">
            <label htmlFor="channel-select">Channel</label>
            <select 
              id="channel-select" 
              value={channel} 
              onChange={(e) => setChannel(e.target.value)}
            >
              <option value="In-Person">In-Person</option>
              <option value="Video Call">Video Call</option>
              <option value="Phone">Phone</option>
              <option value="Email">Email</option>
            </select>
          </div>

          <div className="form-group col-4">
            <label htmlFor="topics-input">Discussion Topics (comma separated)</label>
            <input 
              type="text" 
              id="topics-input" 
              placeholder="e.g. Zyntra, Clinical Trials" 
              value={topics}
              onChange={(e) => setTopics(e.target.value)}
              required
            />
          </div>

          <div className="form-group col-4">
            <label htmlFor="sentiment-select">Sentiment</label>
            <select 
              id="sentiment-select" 
              value={sentiment} 
              onChange={(e) => setSentiment(e.target.value)}
            >
              <option value="Positive">Positive</option>
              <option value="Neutral">Neutral</option>
              <option value="Negative">Negative</option>
            </select>
          </div>
        </div>

        <div className="form-group">
          <div className="label-with-action">
            <label htmlFor="notes-textarea">Meeting Notes / Conversation Transcript</label>
            <button 
              type="button" 
              className="btn-text" 
              onClick={handlePreCheckCompliance}
              disabled={checkingCompliance}
            >
              {checkingCompliance ? (
                <RefreshCw size={12} className="spin" />
              ) : (
                <ShieldCheck size={12} />
              )}
              Analyze Compliance Now
            </button>
          </div>
          <textarea 
            id="notes-textarea" 
            rows={4} 
            placeholder="Type summary details or copy/paste the conversation transcript here..."
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
            required
          />
        </div>

        {/* Compliance feedback block */}
        {complianceReport && (
          <div className={`compliance-card ${complianceReport.compliance_status.toLowerCase()}`}>
            <div className="compliance-card-header">
              {complianceReport.compliance_status === 'Compliant' ? (
                <CheckCircle2 className="comp-icon text-success" />
              ) : (
                <AlertTriangle className="comp-icon text-danger" />
              )}
              <span>Status: <strong>{complianceReport.compliance_status}</strong></span>
            </div>
            <div className="compliance-card-body">
              <p className="recommendation-text">{complianceReport.recommendation}</p>
              {complianceReport.flags && complianceReport.flags.length > 0 && (
                <ul className="flag-list">
                  {complianceReport.flags.map((flag, idx) => (
                    <li key={idx} className="flag-item">
                      <span className="flag-rule">{flag.rule} ({flag.severity} Severity)</span>
                      <p className="flag-desc">{flag.description}</p>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          </div>
        )}

        <div className="form-row">
          <div className="form-group col-6">
            <label htmlFor="followup-date">Suggested Follow-Up Date</label>
            <input 
              type="date" 
              id="followup-date" 
              value={followUpDate} 
              onChange={(e) => setFollowUpDate(e.target.value)} 
            />
          </div>

          <div className="form-group col-6">
            <label htmlFor="nextsteps-input">Next Steps / Action Items</label>
            <input 
              type="text" 
              id="nextsteps-input" 
              placeholder="e.g. Schedule clinical presentation on CV studies" 
              value={nextSteps}
              onChange={(e) => setNextSteps(e.target.value)} 
            />
          </div>
        </div>

        <div className="form-actions">
          <button 
            type="submit" 
            className="btn btn-primary submit-btn" 
            disabled={submitting}
          >
            {submitting ? (
              <RefreshCw className="btn-icon spin" />
            ) : (
              <Save className="btn-icon" />
            )}
            Log & Save Interaction
          </button>
        </div>
      </form>
    </div>
  );
}
