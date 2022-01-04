<template>

  <KModal
    :title="$tr('modalTitle')"
    size="medium"
    :submitText="coreString('confirmAction')"
    :cancelText="coreString('cancelAction')"
    @submit="$emit('submit')"
    @cancel="$emit('cancel')"
  >
    {{ $tr('confirmationMessage') }}
    <p>
      {{ $tr('description') }}
    </p>
  </KModal>

</template>


<script>

  import commonCoreStrings from 'kolibri.coreVue.mixins.commonCoreStrings';

  export default {
    name: 'MatchupResetModal',
    mixins: [commonCoreStrings],
    $trs: {
      modalTitle: {
        message: 'Reset matchup',
        context: "Title of the 'Refresh Matchup' window",
      },
      confirmationMessage: {
        message: 'Are you sure?',
        context: 'Message that displays if user tries to refresh matchup for a subject',
      },
      description: {
        message: ' All saved matchup data will be lost and students will be reassigned.',
        context: 'Message that displays if user tries to refresh matchup for a subject',
      },
    },
  };

</script>


<style lang="scss" scoped></style>
