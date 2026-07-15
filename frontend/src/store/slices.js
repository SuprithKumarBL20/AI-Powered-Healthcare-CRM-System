import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';

// API endpoints prefix is mapped via Vite proxy to http://localhost:8000
const API_URL = '';

// --- ASYNC THUNKS ---

// Fetch all HCPs
export const fetchHcps = createAsyncThunk('hcp/fetchHcps', async (_, { rejectWithValue }) => {
  try {
    const response = await axios.get(`${API_URL}/api/hcps`);
    return response.data;
  } catch (error) {
    return rejectWithValue(error.response?.data?.detail || 'Failed to fetch HCPs');
  }
});

// Fetch all Interactions
export const fetchInteractions = createAsyncThunk('interaction/fetchInteractions', async (_, { rejectWithValue }) => {
  try {
    const response = await axios.get(`${API_URL}/api/interactions`);
    return response.data;
  } catch (error) {
    return rejectWithValue(error.response?.data?.detail || 'Failed to fetch interactions');
  }
});

// Log a new interaction (Structured Form)
export const logInteractionThunk = createAsyncThunk('interaction/logInteraction', async (interactionData, { dispatch, rejectWithValue }) => {
  try {
    const response = await axios.post(`${API_URL}/api/interactions`, interactionData);
    dispatch(fetchInteractions());
    dispatch(fetchHcps()); // Refresh HCP list (to get updated Next Best Action)
    return response.data;
  } catch (error) {
    return rejectWithValue(error.response?.data?.detail || 'Failed to log interaction');
  }
});

// Edit an interaction
export const editInteractionThunk = createAsyncThunk('interaction/editInteraction', async ({ id, updates }, { dispatch, rejectWithValue }) => {
  try {
    const response = await axios.put(`${API_URL}/api/interactions/${id}`, updates);
    dispatch(fetchInteractions());
    return response.data;
  } catch (error) {
    return rejectWithValue(error.response?.data?.detail || 'Failed to update interaction');
  }
});

// Delete an interaction
export const deleteInteractionThunk = createAsyncThunk('interaction/deleteInteraction', async (id, { dispatch, rejectWithValue }) => {
  try {
    await axios.delete(`${API_URL}/api/interactions/${id}`);
    dispatch(fetchInteractions());
    return id;
  } catch (error) {
    return rejectWithValue(error.response?.data?.detail || 'Failed to delete interaction');
  }
});

// Send Chat message to LangGraph Agent
export const sendMessageToAgent = createAsyncThunk('chat/sendMessage', async ({ messages, hcpId }, { rejectWithValue }) => {
  try {
    const response = await axios.post(`${API_URL}/api/chat`, { messages, hcp_id: hcpId });
    return response.data; // returns { response, extracted_state, compliance_check, recommendations }
  } catch (error) {
    return rejectWithValue(error.response?.data?.detail || 'AI Agent failed to respond');
  }
});

// --- SLICES ---

// HCP Slice
const hcpSlice = createSlice({
  name: 'hcp',
  initialState: {
    list: [],
    selectedHcpId: null,
    loading: false,
    error: null,
  },
  reducers: {
    setSelectedHcpId: (state, action) => {
      state.selectedHcpId = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchHcps.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchHcps.fulfilled, (state, action) => {
        state.loading = false;
        state.list = action.payload;
        if (action.payload.length > 0 && !state.selectedHcpId) {
          state.selectedHcpId = action.payload[0].id;
        }
      })
      .addCase(fetchHcps.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  },
});

// Interaction Slice
const interactionSlice = createSlice({
  name: 'interaction',
  initialState: {
    list: [],
    loading: false,
    error: null,
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchInteractions.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchInteractions.fulfilled, (state, action) => {
        state.loading = false;
        state.list = action.payload;
      })
      .addCase(fetchInteractions.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(logInteractionThunk.pending, (state) => {
        state.loading = true;
      })
      .addCase(logInteractionThunk.fulfilled, (state) => {
        state.loading = false;
      })
      .addCase(logInteractionThunk.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  },
});

// Chat Slice
const chatSlice = createSlice({
  name: 'chat',
  initialState: {
    messages: [
      {
        role: 'assistant',
        content: 'Hello! I am your AI CRM Assistant. Select an HCP on the left panel, and tell me details about your recent interaction to log it. You can say: "Log an in-person meeting with Dr. Jenkins today discussing Zyntra. She was positive and wants a clinical trial brochure."',
      },
    ],
    extractedState: null,
    complianceCheck: null,
    recommendations: [],
    loading: false,
    error: null,
  },
  reducers: {
    addMessage: (state, action) => {
      state.messages.push(action.payload);
    },
    clearChat: (state) => {
      state.messages = [
        {
          role: 'assistant',
          content: 'Chat history cleared. How can I assist you with HCP interactions today?',
        },
      ];
      state.extractedState = null;
      state.complianceCheck = null;
      state.recommendations = [];
    },
    setExtractedState: (state, action) => {
      state.extractedState = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(sendMessageToAgent.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(sendMessageToAgent.fulfilled, (state, action) => {
        state.loading = false;
        // Add AI response message
        state.messages.push({
          role: 'assistant',
          content: action.payload.response,
        });
        
        // Sync AI extracted parameters and evaluations
        if (action.payload.extracted_state && Object.keys(action.payload.extracted_state).length > 0) {
          state.extractedState = action.payload.extracted_state;
        }
        if (action.payload.compliance_check && Object.keys(action.payload.compliance_check).length > 0) {
          state.complianceCheck = action.payload.compliance_check;
        }
        if (action.payload.recommendations && action.payload.recommendations.length > 0) {
          state.recommendations = [...state.recommendations, ...action.payload.recommendations];
        }
      })
      .addCase(sendMessageToAgent.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
        state.messages.push({
          role: 'assistant',
          content: `Sorry, I encountered an issue: ${action.payload}`,
        });
      });
  },
});

// UI Slice for Toasts, Custom Confirmations, and Email Modals
const uiSlice = createSlice({
  name: 'ui',
  initialState: {
    toasts: [],
    confirmModal: {
      isOpen: false,
      title: '',
      message: '',
      onConfirmType: null, // 'reset_db', 'delete_interaction', 'complete_task'
      targetId: null,
    },
    emailModal: {
      isOpen: false,
      title: '',
      emailContent: '',
    },
    seeding: false,
  },
  reducers: {
    addToast: (state, action) => {
      state.toasts.push(action.payload);
    },
    removeToast: (state, action) => {
      state.toasts = state.toasts.filter((t) => t.id !== action.payload);
    },
    openConfirm: (state, action) => {
      state.confirmModal = {
        isOpen: true,
        title: action.payload.title,
        message: action.payload.message,
        onConfirmType: action.payload.onConfirmType,
        targetId: action.payload.targetId || null,
      };
    },
    closeConfirm: (state) => {
      state.confirmModal.isOpen = false;
    },
    openEmail: (state, action) => {
      state.emailModal = {
        isOpen: true,
        title: action.payload.title,
        emailContent: action.payload.emailContent,
      };
    },
    closeEmail: (state) => {
      state.emailModal.isOpen = false;
    },
    setSeeding: (state, action) => {
      state.seeding = action.payload;
    }
  }
});

// Toast with automatic dismissal helper
export const showToast = (message, type = 'info') => (dispatch) => {
  const id = Math.random().toString(36).substr(2, 9);
  dispatch(addToast({ id, message, type }));
  setTimeout(() => {
    dispatch(removeToast(id));
  }, 4000);
};

// Export reducers
export const hcpReducer = hcpSlice.reducer;
export const interactionReducer = interactionSlice.reducer;
export const chatReducer = chatSlice.reducer;
export const uiReducer = uiSlice.reducer;

// Export actions
export const { setSelectedHcpId } = hcpSlice.actions;
export const { addMessage, clearChat, setExtractedState } = chatSlice.actions;
export const { addToast, removeToast, openConfirm, closeConfirm, openEmail, closeEmail, setSeeding } = uiSlice.actions;

