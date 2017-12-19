<template>
<div v-if="isLoaded">
  <h2 class="ua__title">Fate</h2>
  <div class="ua__container">
    <div v-for="(calendar, name) in calendars" class="ua__calendar">
      <h3 class="ua__cal-title"j>{{ name }}</h3>
      <div v-for="event in calendar" class="ua__event">
        <h4>{{ event.name }}</h4>
        <p>{{ event.start_time|time }} - {{ event.end_time|time }}</p>
      </div>
      </div>
    </div>
  </div>
</div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'upcoming-appointments',
  created() {
    const vthis = this;
    return axios.get('/start-api/v1/cal')
      .then((response) => {
        const data = response.data;
        Object.keys(data).forEach((key) => {
          data[key].sort((a, b) => {
            const aStart = new Date(a.start_time);
            const bStart = new Date(b.start_time);
            if (aStart > bStart) return 1;
            if (aStart < bStart) return -1;
            return 0;
          });
        });
        vthis.calendars = data;
        vthis.isLoaded = true;
      });
  },
  data() {
    return {
      isLoaded: false,
      calendars: {},
    };
  },
  filters: {
    time(value) {
      return (new Date(value).toLocaleTimeString('en-us'));
    },
  },
};
</script>

<style lang="scss" scoped>
@import "../styles/global.scss";
.ua {
    &__title {
        @include shadow;
        font-size: 3rem;
        margin-top: 8rem;
    }
    &__container {
        background-color: $bg-color-light;
        color: $fg-color-dusky-purple;
        margin: 16px 0 0 0;
        display: flex;
        flex-wrap: wrap;
        align-items: stretch;
    }
    &__calendar {
        padding: 2rem;
        width: calc(33% - 4rem);
        max-width: calc(33% - 4rem);
        @include breakpoint(xs) {
            width: calc(100% - 4rem);
        }
    }
    &__cal-title {
        font-size: 1.8rem;
        color: $fg-color-gray;
        padding: 1rem 0;
    }
    &__event {
        margin-bottom: 1rem;
    }
}
</style>
