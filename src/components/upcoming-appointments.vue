<template>
<div class="ua" v-if="isLoaded">
  <h2 class="ua__title"><span class="fas fa-hourglass-half"></span> Fate</h2>
  <div class="ua__container">
    <div v-for="(calendar, name) in calendars" class="ua__calendar">
      <h3 class="ua__cal-title"j>{{ name }}</h3>
      <div v-for="event in calendar" class="ua__event">
        <h4>
          <span v-if="event.all_day"><span class="fas fa-sun"></span> </span>
          {{ event.name }}
        </h4>
        <p class="ua__times">
          <i v-if="!event.all_day">
            {{ event.start_time|time }} - {{ event.end_time|time }}
          </i>
        </p>
        <div v-if="event.location" class="ua__location">
          <div>
            <span class="fas fa-location-arrow"></span>
          </div>
          <div v-html="linkify(event.location)">
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
</template>

<script>
import axios from 'axios';
import anchorme from 'anchorme';

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
  methods: {
    linkify(value) {
      return anchorme(value);
    },
  },
  filters: {
    time(value) {
      return (new Date(value).toLocaleTimeString('en-us'));
    },
  },
};
</script>

<style lang="scss">
@import "../styles/global.scss";
.ua {
    a:hover {
        color: $fg-color-gray;
    }
    a {
        color: $fg-color-dusky-purple;
    }
    &__title {
        @include shadow;
        font-size: 3rem;
        margin-top: 8rem;
    }

    &__container {
        // Permalink - use to edit and share this gradient:
        // http://colorzilla.com/gradient-editor/#483c4b+0,a47ea5+1,79567a+62&0.9+0,0.9+62
        background: -moz-radial-gradient(center, ellipse cover, rgba(92,80,95,0.9) 0%, rgba(121,86,122,0.9) 70%);
        background: -webkit-radial-gradient(center, ellipse cover, rgba(92,80,95,0.9), rgba(121,86,122,0.9) 70%);
        background: radial-gradient(ellipse at center, rgba(92,80,95,0.9) 0%, rgba(121,86,122,0.9) 70%); 
        color: $fg-color-dusky-purple;
        margin: 16px 0 0 0;
        display: flex;
        flex-wrap: wrap;
        align-items: stretch;
    }

    &__calendar {
        @include breakpoint(xs) {
            width: calc(100% - 4rem);
            max-width: calc(100% - 4rem);
        }
        padding: 2rem;
        width: calc(50% - 4rem);
        max-width: calc(50% - 4rem);
    }

    &__cal-title {
        font-size: 1.8rem;
        color: $fg-color-gray;
        padding: 1rem 0;
    }

    &__event {
        margin-bottom: 1rem;
    }
    &__times {
        font-size: .8rem;
        padding-top: 4px;
    }
    &__location {
        display: flex;
        padding-top: 8px;
        div {
            padding-right: 4px;
        }
    }
}
</style>
