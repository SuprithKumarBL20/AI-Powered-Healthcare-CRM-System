import React from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { setSelectedHcpId } from '../store/slices.js';
import { User, MapPin, Mail, Phone, Sparkles, Award } from 'lucide-react';

export default function HcpSelector() {
  const dispatch = useDispatch();
  const { list: hcps, selectedHcpId, loading } = useSelector((state) => state.hcp);

  if (loading && hcps.length === 0) {
    return (
      <div className="hcp-list-panel loading-state">
        <div className="skeleton skeleton-card"></div>
        <div className="skeleton skeleton-card"></div>
        <div className="skeleton skeleton-card"></div>
      </div>
    );
  }

  const selectedHcp = hcps.find((h) => h.id === selectedHcpId);

  return (
    <aside className="hcp-sidebar">
      <div className="sidebar-section-title">
        <Award className="section-icon" />
        <h2>Healthcare Professionals</h2>
      </div>

      <div className="hcp-list">
        {hcps.map((hcp) => {
          const isSelected = hcp.id === selectedHcpId;
          return (
            <div
              key={hcp.id}
              className={`hcp-item ${isSelected ? 'selected' : ''}`}
              onClick={() => dispatch(setSelectedHcpId(hcp.id))}
            >
              <div className="hcp-avatar">
                <User size={18} />
              </div>
              <div className="hcp-item-details">
                <div className="hcp-name-row">
                  <span className="hcp-name">{hcp.name}</span>
                </div>
                <span className="hcp-specialty-badge">{hcp.specialty}</span>
              </div>
            </div>
          );
        })}
      </div>

      {selectedHcp && (
        <div className="hcp-profile-card">
          <div className="card-header">
            <h3>HCP Profile Card</h3>
          </div>
          <div className="card-body">
            <h4 className="profile-name">{selectedHcp.name}</h4>
            <div className="profile-specialty-meta">
              <span className="badge-primary">{selectedHcp.specialty}</span>
            </div>

            <div className="profile-details-list">
              <div className="profile-detail-item">
                <MapPin size={16} className="item-icon" />
                <span>{selectedHcp.hospital || 'N/A'}</span>
              </div>
              <div className="profile-detail-item">
                <Mail size={16} className="item-icon" />
                <span>{selectedHcp.email || 'N/A'}</span>
              </div>
              <div className="profile-detail-item">
                <Phone size={16} className="item-icon" />
                <span>{selectedHcp.phone || 'N/A'}</span>
              </div>
            </div>

            {selectedHcp.next_best_action && (
              <div className="nba-container">
                <div className="nba-title">
                  <Sparkles size={14} className="nba-icon animate-pulse" />
                  <span>AI NEXT BEST ACTION</span>
                </div>
                <p className="nba-content">{selectedHcp.next_best_action}</p>
              </div>
            )}
            
            {selectedHcp.notes && (
              <div className="hcp-notes-section">
                <strong>HCP Preferences:</strong>
                <p>{selectedHcp.notes}</p>
              </div>
            )}
          </div>
        </div>
      )}
    </aside>
  );
}
