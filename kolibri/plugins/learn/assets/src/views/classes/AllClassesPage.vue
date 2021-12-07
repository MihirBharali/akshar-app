<template>

  <div>
    <div v-if="isUserLoggedIn ">

      <h2>
        <KLabeledIcon icon="classes" :label="$tr('yourClassesHeader')" />
      </h2>
      <CardGrid v-if="classrooms.length > 0" :gridType="2">
        <CardLink
          v-for="c in classrooms"
          :key="c.id"
          :to="classAssignmentsLink(c.id)"
        >
          {{ c.name }} 
        </CardLink>
      </CardGrid>

      <p v-else>
        {{ $tr('noClasses') }}
      </p>

      <div v-if="hasNotifications">

        <NotificationBlock />

      </div>
      <div v-if="hasMatchups">
        <h2>
          <KLabeledIcon icon="device" :label="$tr('yourMatchupsHeader')" />
        </h2>
        <CardGrid v-if="matchupSubjects.length > 0" :gridType="2">
          <CardLink
            v-for="subject in matchupSubjects"
            :key="subject"
            :to="matchupDetailsLink(subject)"
          >
            {{ subject }} 
          </CardLink>
        </CardGrid>
      </div>
    </div>


    <AuthMessage v-else authorizedRole="learner" />
  </div>

</template>


<script>

  import { mapState, mapGetters } from 'vuex';
  import AuthMessage from 'kolibri.coreVue.components.AuthMessage';
  import commonCoreStrings from 'kolibri.coreVue.mixins.commonCoreStrings';
  import CardGrid from '../cards/CardGrid.vue';
  import CardLink from '../cards/CardLink.vue';
  import NotificationBlock from '../cards/NotificationBlock.vue';
  import { classAssignmentsLink, matchupDetailsLink } from './classPageLinks';

  export default {
    name: 'AllClassesPage',
    metaInfo() {
      return {
        title: this.coreString('classesLabel'),
      };
    },
    components: {
      AuthMessage,
      CardLink,
      CardGrid,
      NotificationBlock,
    },
    mixins: [commonCoreStrings],
    computed: {
      ...mapGetters(['isUserLoggedIn']),
      ...mapState('classes', ['classrooms', 'notifications', 'matchups']),
      hasNotifications() {
        if (this.notifications === undefined) {
          return false;
        }
        return Object.keys(this.notifications).length > 0;
      },
      hasMatchups() {
        console.log(this.matchups);
        if (this.matchups === undefined) {
          return false;
        }
        return Object.keys(this.matchups).length > 0;
      },
      matchupSubjects() {
        let subjects = [];
        for (var i in this.matchups) {
          if (subjects.indexOf(this.matchups[i]['subject'] == -1)) {
            let subject = this.matchups[i]['subject'];
            if (subject !== undefined) {
              subjects.push(subject);
            }
          }
        }
        return subjects;
      },
    },
    methods: {
      classAssignmentsLink,
      matchupDetailsLink,
    },
    $trs: {
      yourClassesHeader: 'Your classes',
      yourNotificationsHeader: 'Your notifications',
      yourMatchupsHeader: 'Your matchups',
      noClasses: {
        message: 'You are not enrolled in any classes',
        context:
          'Message that a learner sees in the Learn > CLASSES section if they are not enrolled in any classes.',
      },
    },
  };

</script>


<style lang="scss" scoped></style>
