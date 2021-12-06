import _head from 'lodash/head';
import { AdminMatchupResource } from 'kolibri.resources';
import { DEFAULT_SELECTED_SUBJECT } from '../../views/MatchUpPage/constants';

export function showMatchUpPage(store, toRoute) {
  const { facility_id } = toRoute.params;
  const facilityId = facility_id || store.getters.activeFacilityId;
  const defaultSelectedSubject = DEFAULT_SELECTED_SUBJECT;
  store.dispatch('preparePage', { isAsync: false });

  return AdminMatchupResource.fetchCollection({
    getParams: { facility: facilityId, subject: defaultSelectedSubject },
  })
    .then(data => {
      store.commit('matchup/SET_MATCH_UP_DATA', _head(data));
      store.commit('CORE_SET_PAGE_LOADING', false);
    })
    .catch(error => {
      store.dispatch('handleApiError', error);
      store.commit('matchup/SET_MATCH_UP_DATA', {});
      store.commit('CORE_SET_PAGE_LOADING', false);
    });
}
