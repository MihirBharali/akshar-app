<template>

  <Navbar>
    <NavbarLink
      v-if="showClassesLink"
      name="classes-link"
      :title="coreString('classesLabel')"
      :link="allClassesLink"
    >
      <KIcon
        icon="classes"
        style="top: 0; width: 24px; height: 24px;"
        :color="$themeTokens.textInverted"
      />
    </NavbarLink>
    <NavbarLink
      v-if="canAccessUnassignedContent"
      :title="coreString('channelsLabel')"
      :link="channelsLink"
    >
      <KIcon
        icon="channel"
        style="top: 0; width: 24px; height: 24px;"
        :color="$themeTokens.textInverted"
      />
    </NavbarLink>
    <NavbarLink
      v-if="canAccessUnassignedContent"
      :title="learnString('recommendedLabel')"
      :link="recommendedLink"
    >
      <KIcon
        icon="recommended"
        style="top: 0; width: 24px; height: 24px;"
        :color="$themeTokens.textInverted"
      />
    </NavbarLink>
    <NavbarLink
      :title="$tr('match_up')"
      :link="matchupLink"
    >
      <KIcon
        icon="device"
        style="top: 0; width: 24px; height: 24px;"
        :color="$themeTokens.textInverted"
      />
    </NavbarLink>
    <NavbarLink
      :title="$tr('wage')"
      :link="wagePageLink"
    >
      <KIcon
        icon="star"
        style="top: 0; width: 24px; height: 24px;"
        :color="$themeTokens.textInverted"
      />
    </NavbarLink>
  </Navbar>

</template>


<script>

  import { mapGetters, mapState } from 'vuex';
  import Navbar from 'kolibri.coreVue.components.Navbar';
  import NavbarLink from 'kolibri.coreVue.components.NavbarLink';
  import commonCoreStrings from 'kolibri.coreVue.mixins.commonCoreStrings';
  import { ClassesPageNames, PageNames } from '../constants';
  import commonLearnStrings from './commonLearnStrings';

  export default {
    name: 'LearnTopNav',
    components: {
      Navbar,
      NavbarLink,
    },
    mixins: [commonCoreStrings, commonLearnStrings],
    data() {
      return {
        allClassesLink: {
          name: ClassesPageNames.ALL_CLASSES,
        },
        channelsLink: {
          name: PageNames.TOPICS_ROOT,
        },
        recommendedLink: {
          name: PageNames.RECOMMENDED,
        },
        matchupLink: {
          name: ClassesPageNames.MATCHUP_DETAILS,
        },
        wagePageLink: {
          name: PageNames.WAGE_DETAILS,
        },
      };
    },
    computed: {
      ...mapGetters(['isUserLoggedIn', 'canAccessUnassignedContent']),
      ...mapState({
        userHasMemberships: state => state.memberships.length > 0,
      }),
      showClassesLink() {
        return this.isUserLoggedIn && (this.userHasMemberships || !this.canAccessUnassignedContent);
      },
    },
    $trs: {
      match_up: {
        message: 'Match Up',
        context: "Title of tab in 'Learner' section.",
      },
      wage: {
        message: 'Wage',
        context: "Title of tab in 'Learner' section.",
      },
    },
  };

</script>


<style lang="scss" scoped></style>
