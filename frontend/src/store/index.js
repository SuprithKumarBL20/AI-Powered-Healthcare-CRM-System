import { configureStore } from '@reduxjs/toolkit';
import { hcpReducer, interactionReducer, chatReducer, uiReducer } from './slices.js';

export const store = configureStore({
  reducer: {
    hcp: hcpReducer,
    interaction: interactionReducer,
    chat: chatReducer,
    ui: uiReducer,
  },
});
