import { useState, useEffect } from 'react';
import axios from 'axios';
import { 
  Briefcase, 
  RefreshCw, 
  UploadCloud, 
  Search, 
  MapPin, 
  Calendar, 
  GraduationCap,
  Download,
  Building,
  CheckCircle,
  ExternalLink,
  Code
} from 'lucide-react';
import './index.css';

const API_BASE = 'http://localhost:8000/api';

function App() {
  const [jobs, setJobs] = useState([]);
  const [stats, setStats] = useState({ total: 0, tnJobs: 0, lastUpdated: 'Never' });
  const [loading, setLoading] = useState(false);
  const [syncing, setSyncing] = useState(false);
  const [search, setSearch] = useState('');
  const [notification, setNotification] = useState(null);

  const fetchJobs = async () => {
    try {
      const { data } = await axios.get(`${API_BASE}/jobs`);
      setJobs(data.jobs || []);
      setStats({
        total: data.total_jobs || 0,
        tnJobs: data.tn_jobs || 0,
        lastUpdated: data.last_updated ? new Date(data.last_updated).toLocaleString() : 'Never'
      });
    } catch (err) {
      showNotification('Failed to connect to backend', 'error');
    }
  };

  useEffect(() => {
    fetchJobs();
  }, []);

  const handleScrape = async () => {
    setLoading(true);
    try {
      const { data } = await axios.post(`${API_BASE}/scrape`);
      if (data.success) {
        showNotification(`Successfully scraped ${data.jobs_count} fresh jobs`, 'success');
        fetchJobs();
      } else {
        showNotification(data.message, 'error');
      }
    } catch (err) {
      showNotification('Scraping failed', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleSync = async () => {
    setSyncing(true);
    try {
      const { data } = await axios.post(`${API_BASE}/sync`);
      if (data.success) {
        showNotification(`Successfully synced to Google Sheets. Inserted: ${data.inserted}`, 'success');
      } else {
        showNotification(data.message, 'error');
      }
    } catch (err) {
      showNotification('Sync failed. Check credentials.json', 'error');
    } finally {
      setSyncing(false);
    }
  };

  const showNotification = (message, type) => {
    setNotification({ message, type });
    setTimeout(() => setNotification(null), 5000);
  };

  const exportCSV = () => {
    if (jobs.length === 0) return;
    
    const headers = ['S.No', 'Company Name', 'Category', 'Location', 'Last Date to Apply', 'Batch', 'Qualification / Experience', 'Required Skills', 'Apply Link', 'Job / Internship'];
    const csvContent = [
      headers.join(','),
      ...jobs.map((job, i) => [
        i + 1,
        `"${job['Company Name'] || ''}"`,
        `"${job['Category'] || ''}"`,
        `"${job['Location'] || ''}"`,
        `"${job['Last Date to Apply'] || ''}"`,
        `"${job['Batch'] || ''}"`,
        `"${job['Qualification / Experience'] || ''}"`,
        `"${job['Required Skills'] || ''}"`,
        `"${job['Apply Link'] || ''}"`,
        `"${job['Job / Internship'] || ''}"`
      ].join(','))
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.setAttribute("download", `jobs_export_${new Date().toISOString().split('T')[0]}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const filteredJobs = jobs.filter(job => 
    (job['Company Name'] || '').toLowerCase().includes(search.toLowerCase()) ||
    (job['Original Title'] || '').toLowerCase().includes(search.toLowerCase()) ||
    (job['Location'] || '').toLowerCase().includes(search.toLowerCase()) ||
    (job['Required Skills'] || '').toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="container">
      <header className="header">
        <div>
          <h1 className="title">Freshers Job Auto Finder</h1>
          <p className="subtitle">AI-Powered Scraping Engine for freshershunt.in</p>
        </div>
        <div className="header-status">
          <p className="subtitle" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', justifyContent: 'flex-end' }}>
            <span className="status-dot"></span> Live System Active
          </p>
          <p style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', marginTop: '0.25rem' }}>
            Next auto-sync: 8:00 AM
          </p>
        </div>
      </header>

      <div className="stats-grid">
        <div className="stat-card">
          <span className="stat-label">Total Jobs Found</span>
          <span className="stat-value">{stats.total}</span>
          <span className="subtitle" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Briefcase size={14} /> Active Listings
          </span>
        </div>
        <div className="stat-card" style={{ borderColor: 'var(--success-bg)' }}>
          <span className="stat-label">Tamil Nadu Prioritized</span>
          <span className="stat-value" style={{ color: 'var(--success)' }}>{stats.tnJobs}</span>
          <span className="subtitle" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <MapPin size={14} color="var(--success)" /> Matching Location
          </span>
        </div>
        <div className="stat-card">
          <span className="stat-label">Last Updated Time</span>
          <span className="stat-value" style={{ fontSize: '1.5rem', lineHeight: '2.5rem' }}>
            {stats.lastUpdated !== 'Never' ? stats.lastUpdated.split(', ')[1] : '--:--'}
          </span>
          <span className="subtitle" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Calendar size={14} /> {stats.lastUpdated !== 'Never' ? stats.lastUpdated.split(', ')[0] : 'Today'}
          </span>
        </div>
      </div>

      <div className="controls">
        <button className="btn" onClick={handleScrape} disabled={loading || syncing}>
          {loading ? <div className="spinner"></div> : <RefreshCw size={18} />}
          Start Live Scraping
        </button>
        <button className="btn btn-success" onClick={handleSync} disabled={loading || syncing}>
          {syncing ? <div className="spinner"></div> : <UploadCloud size={18} />}
          Auto Sync to Sheets
        </button>
        <button className="btn btn-outline" onClick={exportCSV} disabled={jobs.length === 0}>
          <Download size={18} />
          Export CSV
        </button>
        
        <div className="search-bar">
          <Search size={18} className="search-icon" />
          <input 
            type="text" 
            className="search-input" 
            placeholder="Filter by company, skills, location..." 
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
      </div>

      <div className="jobs-grid">
        {filteredJobs.length === 0 ? (
          <div className="no-jobs">
            <Briefcase size={48} style={{ opacity: 0.3, marginBottom: '1rem' }} />
            <h3>No active jobs found</h3>
            <p>Click "Start Live Scraping" to fetch today's freshest jobs.</p>
          </div>
        ) : (
          filteredJobs.map((job, idx) => (
            <div className="job-card" key={idx}>
              <div className="job-title">{job['Original Title'] || job['Company Name']}</div>
              <div className="job-company">
                <Building size={14} /> 
                {job['Company Name']}
                {job['Location']?.toLowerCase().includes('tamil nadu') && (
                  <span className="job-tag badge-success text-xs ml-auto border-0">🎯 High Priority</span>
                )}
              </div>
              
              <div className="job-tags">
                <span className="job-tag">{job['Category']}</span>
                <span className="job-tag">{job['Job / Internship']}</span>
                <span className="job-tag">{job['Batch']}</span>
              </div>
              
              <div className="job-details">
                <div className="job-detail-item">
                  <MapPin size={12} /> {job['Location']}
                </div>
                <div className="job-detail-item">
                  <GraduationCap size={12} /> {job['Qualification / Experience']}
                </div>
                <div className="job-detail-item" style={{ gridColumn: '1 / -1', alignItems: 'flex-start' }}>
                  <Code size={12} style={{ marginTop: '0.2rem', flexShrink: 0 }} /> 
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.35rem' }}>
                    {job['Required Skills'] ? job['Required Skills'].split(',').map((skill, i) => (
                      <span key={i} className="skill-tag">{skill.trim()}</span>
                    )) : <span className="skill-tag">Not Specified</span>}
                  </div>
                </div>
              </div>
              
              <div className="job-footer">
                <span className="status-badge">
                  <CheckCircle size={14} /> Active
                </span>
                <a 
                  href={job['Apply Link']} 
                  target="_blank" 
                  rel="noreferrer"
                  className="btn" 
                  style={{ padding: '0.4rem 0.75rem', fontSize: '0.75rem' }}
                >
                  View Details <ExternalLink size={12} />
                </a>
              </div>
            </div>
          ))
        )}
      </div>

      {notification && (
        <div className={`notification ${notification.type}`}>
          {notification.type === 'success' ? <CheckCircle size={20} color="var(--success)" /> : <RefreshCw size={20} color="#ef4444" />}
          {notification.message}
        </div>
      )}
    </div>
  );
}

export default App;
