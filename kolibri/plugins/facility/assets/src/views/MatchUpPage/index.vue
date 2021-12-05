<template>

  <div>
    <KPageContainer>
      <h1>{{ $tr('pageHeader') }}</h1>
      <div v-if="!matchupDataAvailable">
        {{ $tr('noMatchUpDataLabel') }}
      </div>
      <div v-if="matchupDataAvailable" class="matchup-deck">
        <div class="unassigned-deck">
          <KSelect
            v-model="selectedSubject"
            :label="$tr('subjectDropdownLabel')"
            :options="subjectOptions"
            @change="handleSubjectChange"
          />
          <div class="unassigned-users-label">
            {{ $tr('unassignedUsersLabel') }}
          </div>
          <FilterTextbox
            v-model.trim="searchedUnassignedUser"
            :placeholder="$tr('searchForUser')"
          />
          <UnassignedUserContainer
            :className="unassignedMentorsClassname"
            :containerLabel="$tr('unassignedMentorsLabel')"
            :users="filteredUnassignedMentors"
          />
          <UnassignedUserContainer
            :className="unassignedMenteesClassname"
            :containerLabel="$tr('unassignedMenteesLabel')"
            :users="filteredUnassignedMentees"
          />
        </div>
        <div class="assigned-deck">
          <SupervisorCard
            v-for="(matchUpDetail, index) in mergedMatchUpDetails"
            :id="matchUpDetail.supervisor.id"
            :key="matchUpDetail.supervisor.id"
            :index="index"
            :name="matchUpDetail.supervisor.name"
            :supervisorMatchups="matchUpDetail.match_up"
            @supervisor-mentor-match-up-update="handleSupervisorMentorMatchupUpdate"
            @mentor-mentee-match-up-update="handleMentorMenteeMatchupUpdate"
            @unassigned-mentor-added="handleUnassignedMentorAddition"
            @unassigned-mentee-added="handleUnassignedMenteeAddition"
            @remove-mentee="handleRemoveMentee"
          />
        </div>
      </div>
      <BottomAppBar v-if="matchupDataAvailable">
        <template>
          <KButtonGroup>
            <KButton :text="$tr('save')" :primary="true" @click="handleSaveMatchupData" />
            <KButton :text="$tr('reset')" @click="handleResetMatchupData" />
          </KButtonGroup>
        </template>
      </BottomAppBar>
    </KPageContainer>
  </div>

</template>


<script>

  import _isNil from 'lodash/isNil';
  import _find from 'lodash/find';
  import _findIndex from 'lodash/findIndex';
  import _get from 'lodash/get';
  import _map from 'lodash/map';
  import _filter from 'lodash/filter';
  import _isEmpty from 'lodash/isEmpty';
  import _includes from 'lodash/includes';
  import _toLower from 'lodash/toLower';
  import _cloneDeep from 'lodash/cloneDeep';
  import _reduce from 'lodash/reduce';
  import _compact from 'lodash/compact';
  import _castArray from 'lodash/castArray';
  import { mapActions, mapGetters } from 'vuex';

  import BottomAppBar from 'kolibri.coreVue.components.BottomAppBar';
  import FilterTextbox from 'kolibri.coreVue.components.FilterTextbox';
  import commonCoreStrings from 'kolibri.coreVue.mixins.commonCoreStrings';
  import SupervisorCard from './components/SupervisorCard';
  import UnassignedUserContainer from './components/UnassignedUserContainer';
  import {
    UNASSIGNED_MENTORS_CLASSNAME,
    UNASSIGNED_MENTEES_CLASSNAME,
    SUBJECTS,
    DEFAULT_SELECTED_SUBJECT,
  } from './constants';

  export default {
    name: 'MatchUpPage',
    components: { SupervisorCard, BottomAppBar, UnassignedUserContainer, FilterTextbox },
    mixins: [commonCoreStrings],
    data() {
      return {
        searchedUnassignedUser: '',
        selectedSubject: {},
        subjectOptions: [],
        unassignedMentorsClassname: UNASSIGNED_MENTORS_CLASSNAME,
        unassignedMenteesClassname: UNASSIGNED_MENTEES_CLASSNAME,
      };
    },
    computed: {
      ...mapGetters('matchup', ['matchupData']),
      ...mapGetters(['activeFacilityId']),
      facilityMatchupData() {
        return this.matchupData;
      },
      matchupDataAvailable() {
        return !_isEmpty(this.matchupData) && !_isNil(this.matchupData);
      },
      matchUpDetails() {
        return _get(this.facilityMatchupData, ['match_up_details'], []);
      },
      unassignedSupervisorList() {
        return _get(this.facilityMatchupData, ['unassigned_pool', 'supervisor_list'], []);
      },
      mergedMatchUpDetails() {
        return this.getMergedMatchupData(this.matchUpDetails, this.unassignedSupervisorList);
      },
      unassignedMentors() {
        return _get(this.facilityMatchupData, ['unassigned_pool', 'mentor_list'], []);
      },
      unassignedMentees() {
        return _get(this.facilityMatchupData, ['unassigned_pool', 'mentee_list'], []);
      },
      filteredUnassignedMentors() {
        if (_isEmpty(this.searchedUnassignedUser)) return this.unassignedMentors;
        return _filter(this.unassignedMentors, mentor =>
          _includes(_toLower(mentor.name), _toLower(this.searchedUnassignedUser))
        );
      },
      filteredUnassignedMentees() {
        if (_isEmpty(this.searchedUnassignedUser)) return this.unassignedMentees;
        return _filter(this.unassignedMentees, mentee =>
          _includes(_toLower(mentee.name), _toLower(this.searchedUnassignedUser))
        );
      },
    },
    created() {
      this.subjectOptions = _reduce(
        SUBJECTS,
        (acc, { label = '', value = '' } = {}) => [...acc, { label, value }],
        []
      );
      this.selectedSubject = _find(this.subjectOptions, { value: DEFAULT_SELECTED_SUBJECT });
    },
    methods: {
      ...mapActions('matchup', ['getMatchupData', 'saveMatchupData']),
      getMergedMatchupData(matchUpDetails, unassignedSupervisorList) {
        const initialData = matchUpDetails;
        const newData = _map(unassignedSupervisorList, supervisor => ({
          supervisor,
          match_up: [],
        }));

        return [...initialData, ...newData];
      },
      handleSupervisorMentorMatchupUpdate(data) {
        const {
          mentorId,
          originSupervisorId,
          destinationSupervisorId,
          originSupervisorIndex,
          destinationSupervisorIndex,
        } = data;
        const currentMatchupData = this.mergedMatchUpDetails;

        if (
          originSupervisorId &&
          destinationSupervisorId &&
          !_isNil(originSupervisorIndex) &&
          !_isNil(destinationSupervisorIndex)
        ) {
          const mentorMatchupIndexInOriginList = _findIndex(
            currentMatchupData[originSupervisorIndex].match_up,
            ({ mentor }) => mentor.id === mentorId
          );
          const mentorMatchupObject = _get(currentMatchupData, [
            originSupervisorIndex,
            'match_up',
            mentorMatchupIndexInOriginList,
          ]);

          currentMatchupData[originSupervisorIndex].match_up.splice(
            mentorMatchupIndexInOriginList,
            1
          );
          currentMatchupData[destinationSupervisorIndex].match_up.push(mentorMatchupObject);
        }
      },
      handleMentorMenteeMatchupUpdate(data) {
        const {
          menteeId,
          originMentorId,
          originMentorIndex,
          originSupervisorId,
          originSupervisorIndex,
          destinationMentorId,
          destinationMentorIndex,
          destinationSupervisorId,
          destinationSupervisorIndex,
        } = data;
        const currentMatchupData = this.mergedMatchUpDetails;

        if (
          originMentorId &&
          originSupervisorId &&
          destinationMentorId &&
          destinationSupervisorId &&
          !_isNil(originMentorIndex) &&
          !_isNil(originSupervisorIndex) &&
          !_isNil(destinationMentorIndex) &&
          !_isNil(destinationSupervisorIndex)
        ) {
          const menteeIndexInOriginList = _findIndex(
            currentMatchupData[originSupervisorIndex].match_up[originMentorIndex].mentee_list,
            mentee => mentee.id === menteeId
          );
          const menteeObject = _get(currentMatchupData, [
            originSupervisorIndex,
            'match_up',
            originMentorIndex,
            'mentee_list',
            menteeIndexInOriginList,
          ]);
          currentMatchupData[originSupervisorIndex].match_up[originMentorIndex].mentee_list.splice(
            menteeIndexInOriginList,
            1
          );
          currentMatchupData[destinationSupervisorIndex].match_up[
            destinationMentorIndex
          ].mentee_list.push(menteeObject);
        }
      },
      handleUnassignedMentorAddition(data) {
        const {
          userId,
          userName,
          userIndex,
          destinationSupervisorId,
          destinationSupervisorIndex,
        } = data;

        if (
          userId &&
          userName &&
          destinationSupervisorId &&
          !_isNil(userIndex) &&
          !_isNil(destinationSupervisorIndex)
        ) {
          const mentorObject = { name: userName, id: userId };
          this.mergedMatchUpDetails[destinationSupervisorIndex].match_up.push({
            mentee_list: [],
            mentor: mentorObject,
          });
          this.unassignedMentors.splice(userIndex, 1);
        }
      },
      handleUnassignedMenteeAddition(data) {
        const {
          userId,
          userName,
          userIndex,
          destinationMentorId,
          destinationMentorIndex,
          destinationSupervisorId,
          destinationSupervisorIndex,
        } = data;

        if (
          userId &&
          userName &&
          destinationMentorId &&
          destinationSupervisorId &&
          !_isNil(userIndex) &&
          !_isNil(destinationMentorIndex) &&
          !_isNil(destinationSupervisorIndex)
        ) {
          const menteeObject = { name: userName, id: userId };
          this.mergedMatchUpDetails[destinationSupervisorIndex].match_up[
            destinationMentorIndex
          ].mentee_list.push(menteeObject);
          this.unassignedMentees.splice(userIndex, 1);
        }
      },
      handleSaveMatchupData() {
        const unassignedMentees = _cloneDeep(this.unassignedMentees);
        let unassignedMentors = _cloneDeep(this.unassignedMentors);
        let unassignedSupervisors = [];
        const finalMatchupData = _reduce(
          this.mergedMatchUpDetails,
          (acc, supervisorMatchup) => {
            let matchUp = _get(supervisorMatchup, 'match_up', []);
            const supervisorData = _get(supervisorMatchup, 'supervisor', {});
            matchUp = _compact(
              _map(matchUp, mentorMatchup => {
                const menteeList = _get(mentorMatchup, 'mentee_list', []);
                const mentorObj = _get(mentorMatchup, 'mentor', {});
                if (_isEmpty(menteeList)) {
                  unassignedMentors.push(mentorObj);
                  return undefined;
                }
                return mentorMatchup;
              })
            );

            if (_isEmpty(matchUp)) {
              unassignedSupervisors.push(supervisorData);
              return acc;
            } else return [...acc, supervisorMatchup];
          },
          []
        );
        const dataToSave = {
          facility_id: this.activeFacilityId,
          subject: this.selectedSubject.value,
          match_up_details: finalMatchupData,
          unassigned_pool: {
            mentee_list: unassignedMentees,
            mentor_list: unassignedMentors,
            supervisor_list: unassignedSupervisors,
          },
        };
        this.saveMatchupData({
          data: dataToSave,
        }).then(() => {
          this.$store.dispatch('createSnackbar', this.coreString('changesSavedNotification'));
        });
      },
      handleRemoveMentee(data) {
        const {
          menteeId,
          originMentorId,
          originMentorIndex,
          originSupervisorId,
          originSupervisorIndex,
        } = data;
        const currentMatchupData = this.mergedMatchUpDetails;

        if (
          originMentorId &&
          originSupervisorId &&
          !_isNil(originMentorIndex) &&
          !_isNil(originSupervisorIndex)
        ) {
          const menteeIndexInOriginList = _findIndex(
            currentMatchupData[originSupervisorIndex].match_up[originMentorIndex].mentee_list,
            mentee => mentee.id === menteeId
          );
          const menteeObject = _get(currentMatchupData, [
            originSupervisorIndex,
            'match_up',
            originMentorIndex,
            'mentee_list',
            menteeIndexInOriginList,
          ]);
          currentMatchupData[originSupervisorIndex].match_up[originMentorIndex].mentee_list.splice(
            menteeIndexInOriginList,
            1
          );
          this.unassignedMentees.push({ ...menteeObject, keepUnassigned: true });
        }
      },
      handleResetMatchupData() {
        this.selectedSubject &&
          this.selectedSubject.value &&
          this.getMatchupData({
            subject: this.selectedSubject.value,
            facility: this.activeFacilityId,
          }).catch(error => {
            this.$store.dispatch('handleApiError', error);
          });
      },
      handleSubjectChange(evt) {
        this.getMatchupData({ subject: evt.value, facility: this.activeFacilityId }).catch(
          error => {
            this.$store.dispatch('handleApiError', error);
          }
        );
      },
    },
    $trs: {
      pageHeader: {
        message: 'Learner Match-up',
        context: 'Description on Facility > Match-up page.',
      },
      noMatchUpDataLabel: {
        message: 'Match-up data is unavailable.',
        context: 'Label used to show match-up data is not available.',
      },
      subjectDropdownLabel: {
        message: 'Selected Subject',
        context: 'Dropdown used to select subject for match-up',
      },
      save: {
        message: 'Save Match-up',
      },
      reset: { message: 'Reset' },
      unassignedUsersLabel: { message: 'Unassigned Users' },
      unassignedMentorsLabel: { message: 'Mentors' },
      unassignedMenteesLabel: { message: 'Mentees' },
      searchForUser: { message: 'Search users' },
    },
  };

</script> 

<style lang="scss" scoped>

  .matchup-deck {
    display: flex;
  }

  .unassigned-deck {
    width: 30%;
    padding: 1rem 1rem 0 0;
    margin-right: 1rem;
    background-color: white;
    border-right: 1px solid #d4d5d6;
  }

  .assigned-deck {
    display: grid;
    grid-template-columns: auto auto auto;
    width: 70%;
  }

  .dragged-mentor {
    opacity: 0.2 !important;
  }

  .unassigned-users-label {
    margin: 1.5rem 0 1rem;
    font-size: 0.9375rem;
    color: #0000008a;
  }

</style>
