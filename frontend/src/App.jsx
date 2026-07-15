import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { 
  fetchHcps, fetchInteractions, 
  closeConfirm, closeEmail, showToast, removeToast, setSeeding,
  deleteInteractionThunk 
} from './store/slices.js';
import axios from 'axios';
import Navbar from './components/Navbar.jsx';
import HcpSelector from './components/HcpSelector.jsx';
import LogInteractionForm from './components/LogInteractionForm.jsx';
import ChatInterface from './components/ChatInterface.jsx';
import HistoryPanel from './components/HistoryPanel.jsx';
import FollowUpPanel from './components/FollowUpPanel.jsx';
import { 
  MessageSquare, LayoutGrid, Settings, AlertTriangle, 
  CheckCircle2, XCircle, Info, X, Mail, Check, RotateCw 
} from 'lucide-react';

export default function App() {
  const dispatch = useDispatch();
  const [loggingMode, setLoggingMode] = useState('chat'); // 'chat' or 'form'

  // Redux UI States
  const toasts = useSelector((state) => state.ui.toasts);
  const confirmModal = useSelector((state) => state.ui.confirmModal);
  const emailModal = useSelector((state) => state.ui.emailModal);

  useEffect(() => {
    dispatch(fetchHcps());
    dispatch(fetchInteractions());
  }, [dispatch]);

  // Global confirm action execution handler
  const handleConfirmAction = async () => {
    const { onConfirmType, targetId } = confirmModal;
    dispatch(closeConfirm());

    try {
      if (onConfirmType === 'reset_db') {
        dispatch(setSeeding(true));
        dispatch(showToast('Resetting database...', 'info'));
        await axios.post('/api/init-db');
        dispatch(fetchHcps());
        dispatch(fetchInteractions());
        dispatch(showToast('Database reset and re-seeded successfully!', 'success'));
        dispatch(setSeeding(false));
      } else if (onConfirmType === 'delete_interaction') {
        dispatch(showToast('Deleting interaction log...', 'info'));
        await dispatch(deleteInteractionThunk(targetId)).unwrap();
        dispatch(showToast('Interaction deleted successfully.', 'success'));
      } else if (onConfirmType === 'complete_task') {
        dispatch(showToast('Updating follow-up status...', 'info'));
        await axios.put(`/api/follow-ups/${targetId}`, { status: 'Completed' });
        dispatch(fetchHcps()); // triggers refresh of lists
        dispatch(showToast('Task marked as Completed!', 'success'));
      }
    } catch (e) {
      console.error(e);
      dispatch(setSeeding(false));
      dispatch(showToast('Action failed to execute.', 'error'));
    }
  };

  return (
    <div className="app-container">
      <Navbar />

      <main className="app-main-layout">
        {/* Sidebar displaying list of HCPs and profile card */}
        <section className="layout-sidebar">
          <HcpSelector />
        </section>

        {/* Central Workspace for interaction logging and histories */}
        <section className="layout-workspace">
          {/* Mode Switcher Header */}
          <div className="workspace-header card">
            <div className="workspace-header-title">
              <Settings className="workspace-header-icon text-primary" />
              <div>
                <h1>Log Interaction Screen</h1>
                <p>Select your preferred logging mode. Both modes are integrated with our PhRMA compliance engine.</p>
              </div>
            </div>

            <div className="mode-toggle-group">
              <button
                className={`mode-btn ${loggingMode === 'chat' ? 'active' : ''}`}
                onClick={() => setLoggingMode('chat')}
              >
                <MessageSquare size={16} className="btn-icon" />
                Conversational AI Logger
              </button>
              <button
                className={`mode-btn ${loggingMode === 'form' ? 'active' : ''}`}
                onClick={() => setLoggingMode('form')}
              >
                <LayoutGrid size={16} className="btn-icon" />
                Structured Form Logger
              </button>
            </div>
          </div>

          {/* Logging Component based on toggle */}
          <div className="logging-workspace">
            {loggingMode === 'chat' ? (
              <ChatInterface />
            ) : (
              <LogInteractionForm />
            )}
          </div>

          {/* History and follow-ups row */}
          <div className="workspace-footer-grid">
            <div className="footer-col">
              <FollowUpPanel />
            </div>
            <div className="footer-col">
              <HistoryPanel />
            </div>
          </div>
        </section>
      </main>

      {/* --- PREMIUM GLOBAL TOASTS CONTAINER --- */}
      <div className="toast-container">
        {toasts.map((toast) => {
          let ToastIcon = Info;
          if (toast.type === 'success') ToastIcon = CheckCircle2;
          if (toast.type === 'error') ToastIcon = XCircle;
          if (toast.type === 'warning') ToastIcon = AlertTriangle;

          return (
            <div key={toast.id} className={`toast-card ${toast.type}`}>
              <ToastIcon size={18} className="toast-card-icon" />
              <div className="toast-card-message">{toast.message}</div>
              <button 
                className="toast-close-btn"
                onClick={() => dispatch(removeToast(toast.id))}
              >
                <X size={14} />
              </button>
              <div className="toast-progress-bar"></div>
            </div>
          );
        })}
      </div>

      {/* --- CUSTOM DIALOGS & OVERLAYS --- */}

      {/* 1. Glassmorphic Confirmation Modal */}
      {confirmModal.isOpen && (
        <div className="modal-overlay">
          <div className="modal-card confirm-modal animate-scaleUp">
            <div className="modal-header">
              <AlertTriangle className="modal-icon text-warning animate-bounce" size={24} />
              <h3>{confirmModal.title}</h3>
            </div>
            <div className="modal-body">
              <p>{confirmModal.message}</p>
            </div>
            <div className="modal-footer">
              <button 
                className="btn btn-secondary btn-sm" 
                onClick={() => dispatch(closeConfirm())}
              >
                Cancel
              </button>
              <button 
                className="btn btn-primary btn-sm btn-danger-action" 
                onClick={handleConfirmAction}
              >
                Confirm Action
              </button>
            </div>
          </div>
        </div>
      )}

      {/* 2. Custom SMTP Dispatch / Email Details Modal */}
      {emailModal.isOpen && (
        <div className="modal-overlay">
          <div className="modal-card email-modal animate-scaleUp">
            <div className="modal-header">
              <Mail className="modal-icon text-primary animate-pulse" size={24} />
              <h3>{emailModal.title}</h3>
            </div>
            <div className="modal-body">
              <p className="email-meta-label">Email successfully sent to HCP with content:</p>
              <pre className="email-modal-preview">{emailModal.emailContent}</pre>
            </div>
            <div className="modal-footer">
              <button 
                className="btn btn-primary btn-sm" 
                onClick={() => dispatch(closeEmail())}
              >
                <Check size={14} className="icon-mr" />
                Done
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
