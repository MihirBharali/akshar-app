import _head from 'lodash/head';
import { AdminMatchupResource } from 'kolibri.resources';

export function getMatchupData(store, payload) {
  return AdminMatchupResource.fetchCollection({
    getParams: payload,
  })
    .then(data => {
      store.commit('SET_MATCH_UP_DATA', _head(data));
    })
    .catch(error => {
      store.commit('SET_MATCH_UP_DATA', {});
      throw error;
    });
}

export function saveMatchupData(store, { id, data }) {
  return AdminMatchupResource.saveModel({
    id,
    data,
  })
    .then(data => {
      store.commit('SET_MATCH_UP_DATA', _head(data));
    })
    .catch(error => {
      store.commit('SET_MATCH_UP_DATA', {});
      throw error;
    });
}
