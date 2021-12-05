import { getMatchupData, saveMatchupData } from './actions';

function defaultState() {
  return {
    matchupData: {},
    selectedSubject: '',
    originalMatchupData: {},
  };
}

export default {
  namespaced: true,
  state: defaultState(),
  mutations: {
    SET_SELECTED_SUBJECT(state, payload) {
      Object.assign(state, { selectedSubject: payload });
    },
    SET_MATCH_UP_DATA(state, payload) {
      Object.assign(state, { matchupData: payload, originalMatchupData: payload });
    },
  },
  getters: {
    selectedSubject: state => state.selectedSubject,
    matchupData: state => state.matchupData,
  },
  actions: {
    getMatchupData,
    saveMatchupData,
  },
};
