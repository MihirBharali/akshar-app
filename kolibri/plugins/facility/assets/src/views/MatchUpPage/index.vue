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
            @remove-mentor="handleRemoveMentor"
          />
        </div>
      </div>
      <BottomAppBar v-if="matchupDataAvailable">
        <template>
          <KButtonGroup>
            <KButton :text="$tr('save')" :primary="true" @click="handleSaveMatchupData" />
            <KButton :text="$tr('refresh')" @click="showMatchupResetConfirmation = true" />
          </KButtonGroup>
        </template>
      </BottomAppBar>
      <MatchupResetModal
        v-if="showMatchupResetConfirmation" 
        @submit="refreshMatchupData" 
        @cancel="showMatchupResetConfirmation = false"
      />
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
  import { mapActions, mapGetters, mapState } from 'vuex';

  import BottomAppBar from 'kolibri.coreVue.components.BottomAppBar';
  import FilterTextbox from 'kolibri.coreVue.components.FilterTextbox';
  import commonCoreStrings from 'kolibri.coreVue.mixins.commonCoreStrings';
  import SupervisorCard from './components/SupervisorCard';
  import MatchupResetModal from './components/MatchupResetModal';
  import UnassignedUserContainer from './components/UnassignedUserContainer';
  import {
    UNASSIGNED_MENTORS_CLASSNAME,
    UNASSIGNED_MENTEES_CLASSNAME,
    SUBJECTS,
    DEFAULT_SELECTED_SUBJECT,
  } from './constants';

  export default {
    name: 'MatchUpPage',
    components: {
      SupervisorCard,
      BottomAppBar,
      UnassignedUserContainer,
      FilterTextbox,
      MatchupResetModal,
    },
    mixins: [commonCoreStrings],
    data() {
      return {
        matchUpDetails: [],
        unassignedSupervisorList: [],
        mergedMatchUpDetails: [],
        unassignedMentors: [],
        unassignedMentees: [],
        searchedUnassignedUser: '',
        selectedSubject: {},
        subjectOptions: [],
        unassignedMentorsClassname: UNASSIGNED_MENTORS_CLASSNAME,
        unassignedMenteesClassname: UNASSIGNED_MENTEES_CLASSNAME,
        showMatchupResetConfirmation: false,
      };
    },
    computed: {
      ...mapState('matchup', ['matchupData', 'originalMatchupData']),
      ...mapGetters(['activeFacilityId']),
      matchupDataAvailable() {
        return !_isEmpty(this.matchupData) && !_isNil(this.matchupData);
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
    mounted() {
      this.init();
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
      init(subjectValue = DEFAULT_SELECTED_SUBJECT) {
        const matchupData = _cloneDeep(this.matchupData);
        this.matchUpDetails = _get(matchupData, ['match_up_details'], []);
        this.unassignedSupervisorList = _get(
          matchupData,
          ['unassigned_pool', 'supervisor_list'],
          []
        );
        this.mergedMatchUpDetails = this.getMergedMatchupData(
          this.matchUpDetails,
          this.unassignedSupervisorList
        );
        this.unassignedMentors = _get(matchupData, ['unassigned_pool', 'mentor_list'], []);
        this.unassignedMentees = _get(matchupData, ['unassigned_pool', 'mentee_list'], []);
        this.subjectOptions = _reduce(
          SUBJECTS,
          (acc, { label = '', value = '' } = {}) => [...acc, { label, value }],
          []
        );
        this.selectedSubject = _find(this.subjectOptions, { value: subjectValue });
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
          userGender,
          userPhysicalFacilityLevel,
          userIndex,
          destinationSupervisorId,
          destinationSupervisorIndex,
        } = data;

        if (
          userId &&
          userName &&
          userGender &&
          destinationSupervisorId &&
          !_isNil(userIndex) &&
          !_isNil(destinationSupervisorIndex)
        ) {
          const mentorObject = {
            name: userName,
            id: userId,
            gender: userGender,
            physical_facility_level: userPhysicalFacilityLevel,
          };
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
          userGender,
          userPhysicalFacilityLevel,
          userIndex,
          destinationMentorId,
          destinationMentorIndex,
          destinationSupervisorId,
          destinationSupervisorIndex,
        } = data;
        console.log(data);
        if (
          userId &&
          userName &&
          destinationMentorId &&
          destinationSupervisorId &&
          !_isNil(userIndex) &&
          !_isNil(destinationMentorIndex) &&
          !_isNil(destinationSupervisorIndex)
        ) {
          const menteeObject = {
            name: userName,
            id: userId,
            gender: userGender,
            physical_facility_level: userPhysicalFacilityLevel,
          };
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
      handleRemoveMentor(data) {
        const { mentorId, originMentorIndex, originSupervisorId, originSupervisorIndex } = data;
        const currentMatchupData = this.mergedMatchUpDetails;

        if (mentorId && originSupervisorId && !_isNil(originSupervisorIndex)) {
          const mentorObject = _get(currentMatchupData, [
            originSupervisorIndex,
            'match_up',
            originMentorIndex,
            'mentor',
          ]);
          currentMatchupData[originSupervisorIndex].match_up.splice(originMentorIndex, 1);
          this.unassignedMentors.push({ ...mentorObject, keepUnassigned: true });
        }
      },
      handleResetMatchupData() {
        this.init(this.selectedSubject.value);
        this.$store.dispatch('createSnackbar', this.$tr('resetMessage'));
      },
      refreshMatchupData() {
        this.showMatchupResetConfirmation = false;
        this.getMatchupData({
          subject: this.selectedSubject.value,
          facility: this.activeFacilityId,
          fullReset: true,
        })
          .then(() => {
            this.$store.dispatch('createSnackbar', this.$tr('resetMessage'));
            this.init(this.selectedSubject.value);
          })
          .catch(error => {
            this.$store.dispatch('handleApiError', error);
          });
      },
    },
    watch: {
      selectedSubject(subject, oldSubject) {
        if (subject.value !== oldSubject.value)
          this.getMatchupData({ subject: subject.value, facility: this.activeFacilityId })
            .then(() => this.init(subject.value))
            .catch(error => {
              this.$store.dispatch('handleApiError', error);
            });
      },
    },
    $trs: {
      pageHeader: {
        message: 'Learner match-up',
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
      refresh: {
        message: 'Reset matchup',
      },
      reset: { message: 'Reset' },
      unassignedUsersLabel: { message: 'Unassigned Users' },
      unassignedMentorsLabel: { message: 'Mentors' },
      unassignedMenteesLabel: { message: 'Mentees' },
      searchForUser: { message: 'Search users' },
      resetMessage: { message: 'Matchup reset' },
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
