// GET /api/gert/events/playback/polar-vortex
// Labeled educational reconstruction. The object matches the companion
// tool response captured on 2026-11-17 from
// https://gert-d.vercel.app/api/gert/events/playback/polar-vortex
// provenance: synthetic_reconstruction.
const PAYLOAD = {
  "event_id": "ercot-2021-educational-reconstruction",
  "title": "ERCOT Polar Vortex \u00b7 Decision Replay",
  "total_hours": 36,
  "steps": [
    {
      "hour": 0,
      "timestamp_label": "Feb 14, 00:00",
      "temperature": 8,
      "actual_load_mw": 49000,
      "capacity_mw": 78500,
      "gert_p99_load_mw": 51300,
      "risk_score": 22
    },
    {
      "hour": 1,
      "timestamp_label": "Feb 14, 01:00",
      "temperature": 5.9,
      "actual_load_mw": 51112,
      "capacity_mw": 77819,
      "gert_p99_load_mw": 53636,
      "risk_score": 28.8
    },
    {
      "hour": 2,
      "timestamp_label": "Feb 14, 02:00",
      "temperature": 3.9,
      "actual_load_mw": 53208,
      "capacity_mw": 77143,
      "gert_p99_load_mw": 55954,
      "risk_score": 35.6
    },
    {
      "hour": 3,
      "timestamp_label": "Feb 14, 03:00",
      "temperature": 1.9,
      "actual_load_mw": 55271,
      "capacity_mw": 76478,
      "gert_p99_load_mw": 58236,
      "risk_score": 42.2
    },
    {
      "hour": 4,
      "timestamp_label": "Feb 14, 04:00",
      "temperature": -0.1,
      "actual_load_mw": 57286,
      "capacity_mw": 75830,
      "gert_p99_load_mw": 60464,
      "risk_score": 48.7
    },
    {
      "hour": 5,
      "timestamp_label": "Feb 14, 05:00",
      "temperature": -2,
      "actual_load_mw": 59237,
      "capacity_mw": 75202,
      "gert_p99_load_mw": 62622,
      "risk_score": 55
    },
    {
      "hour": 6,
      "timestamp_label": "Feb 14, 06:00",
      "temperature": -3.8,
      "actual_load_mw": 61110,
      "capacity_mw": 74602,
      "gert_p99_load_mw": 64692,
      "risk_score": 61
    },
    {
      "hour": 7,
      "timestamp_label": "Feb 14, 07:00",
      "temperature": -5.5,
      "actual_load_mw": 62890,
      "capacity_mw": 74033,
      "gert_p99_load_mw": 66660,
      "risk_score": 66.7
    },
    {
      "hour": 8,
      "timestamp_label": "Feb 14, 08:00",
      "temperature": -7.1,
      "actual_load_mw": 64564,
      "capacity_mw": 73500,
      "gert_p99_load_mw": 68508,
      "risk_score": 72
    },
    {
      "hour": 9,
      "timestamp_label": "Feb 14, 09:00",
      "temperature": -8.6,
      "actual_load_mw": 66118,
      "capacity_mw": 73007,
      "gert_p99_load_mw": 70225,
      "risk_score": 76.9
    },
    {
      "hour": 10,
      "timestamp_label": "Feb 14, 10:00",
      "temperature": -10,
      "actual_load_mw": 67541,
      "capacity_mw": 72558,
      "gert_p99_load_mw": 71796,
      "risk_score": 81.4
    },
    {
      "hour": 11,
      "timestamp_label": "Feb 14, 11:00",
      "temperature": -11.2,
      "actual_load_mw": 68823,
      "capacity_mw": 72157,
      "gert_p99_load_mw": 73209,
      "risk_score": 85.4
    },
    {
      "hour": 12,
      "timestamp_label": "Feb 14, 12:00",
      "temperature": -12.3,
      "actual_load_mw": 69953,
      "capacity_mw": 71807,
      "gert_p99_load_mw": 74455,
      "risk_score": 88.9
    },
    {
      "hour": 13,
      "timestamp_label": "Feb 14, 13:00",
      "temperature": -13.1,
      "actual_load_mw": 70924,
      "capacity_mw": 71512,
      "gert_p99_load_mw": 75523,
      "risk_score": 91.9
    },
    {
      "hour": 14,
      "timestamp_label": "Feb 14, 14:00",
      "temperature": -13.9,
      "actual_load_mw": 71729,
      "capacity_mw": 71272,
      "gert_p99_load_mw": 76406,
      "risk_score": 94.3
    },
    {
      "hour": 15,
      "timestamp_label": "Feb 14, 15:00",
      "temperature": -14.4,
      "actual_load_mw": 72361,
      "capacity_mw": 71091,
      "gert_p99_load_mw": 77098,
      "risk_score": 96.1
    },
    {
      "hour": 16,
      "timestamp_label": "Feb 14, 16:00",
      "temperature": -14.8,
      "actual_load_mw": 72816,
      "capacity_mw": 70969,
      "gert_p99_load_mw": 77594,
      "risk_score": 97.3
    },
    {
      "hour": 17,
      "timestamp_label": "Feb 14, 17:00",
      "temperature": -15,
      "actual_load_mw": 73092,
      "capacity_mw": 70908,
      "gert_p99_load_mw": 77890,
      "risk_score": 97.9
    },
    {
      "hour": 18,
      "timestamp_label": "Feb 14, 18:00",
      "temperature": -15,
      "actual_load_mw": 73187,
      "capacity_mw": 70908,
      "gert_p99_load_mw": 77985,
      "risk_score": 97.9
    },
    {
      "hour": 19,
      "timestamp_label": "Feb 14, 19:00",
      "temperature": -14.8,
      "actual_load_mw": 73101,
      "capacity_mw": 70969,
      "gert_p99_load_mw": 77879,
      "risk_score": 97.3
    },
    {
      "hour": 20,
      "timestamp_label": "Feb 14, 20:00",
      "temperature": -14.4,
      "actual_load_mw": 72836,
      "capacity_mw": 71091,
      "gert_p99_load_mw": 77573,
      "risk_score": 96.1
    },
    {
      "hour": 21,
      "timestamp_label": "Feb 14, 21:00",
      "temperature": -13.9,
      "actual_load_mw": 72394,
      "capacity_mw": 71272,
      "gert_p99_load_mw": 77071,
      "risk_score": 94.3
    },
    {
      "hour": 22,
      "timestamp_label": "Feb 14, 22:00",
      "temperature": -13.1,
      "actual_load_mw": 71779,
      "capacity_mw": 71512,
      "gert_p99_load_mw": 76378,
      "risk_score": 91.9
    },
    {
      "hour": 23,
      "timestamp_label": "Feb 14, 23:00",
      "temperature": -12.3,
      "actual_load_mw": 70998,
      "capacity_mw": 71807,
      "gert_p99_load_mw": 75500,
      "risk_score": 88.9
    },
    {
      "hour": 24,
      "timestamp_label": "Feb 15, 00:00",
      "temperature": -11.2,
      "actual_load_mw": 70058,
      "capacity_mw": 72157,
      "gert_p99_load_mw": 74444,
      "risk_score": 85.4
    },
    {
      "hour": 25,
      "timestamp_label": "Feb 15, 01:00",
      "temperature": -10,
      "actual_load_mw": 68966,
      "capacity_mw": 72558,
      "gert_p99_load_mw": 73221,
      "risk_score": 81.4
    },
    {
      "hour": 26,
      "timestamp_label": "Feb 15, 02:00",
      "temperature": -8.6,
      "actual_load_mw": 67733,
      "capacity_mw": 73007,
      "gert_p99_load_mw": 71840,
      "risk_score": 76.9
    },
    {
      "hour": 27,
      "timestamp_label": "Feb 15, 03:00",
      "temperature": -7.1,
      "actual_load_mw": 66369,
      "capacity_mw": 73500,
      "gert_p99_load_mw": 70313,
      "risk_score": 72
    },
    {
      "hour": 28,
      "timestamp_label": "Feb 15, 04:00",
      "temperature": -5.5,
      "actual_load_mw": 64885,
      "capacity_mw": 74033,
      "gert_p99_load_mw": 68655,
      "risk_score": 66.7
    },
    {
      "hour": 29,
      "timestamp_label": "Feb 15, 05:00",
      "temperature": -3.8,
      "actual_load_mw": 63295,
      "capacity_mw": 74602,
      "gert_p99_load_mw": 66877,
      "risk_score": 61
    },
    {
      "hour": 30,
      "timestamp_label": "Feb 15, 06:00",
      "temperature": -2,
      "actual_load_mw": 61612,
      "capacity_mw": 75202,
      "gert_p99_load_mw": 64997,
      "risk_score": 55
    },
    {
      "hour": 31,
      "timestamp_label": "Feb 15, 07:00",
      "temperature": -0.1,
      "actual_load_mw": 59851,
      "capacity_mw": 75830,
      "gert_p99_load_mw": 63029,
      "risk_score": 48.7
    },
    {
      "hour": 32,
      "timestamp_label": "Feb 15, 08:00",
      "temperature": 1.9,
      "actual_load_mw": 58026,
      "capacity_mw": 76478,
      "gert_p99_load_mw": 60991,
      "risk_score": 42.2
    },
    {
      "hour": 33,
      "timestamp_label": "Feb 15, 09:00",
      "temperature": 3.9,
      "actual_load_mw": 56153,
      "capacity_mw": 77143,
      "gert_p99_load_mw": 58899,
      "risk_score": 35.6
    },
    {
      "hour": 34,
      "timestamp_label": "Feb 15, 10:00",
      "temperature": 5.9,
      "actual_load_mw": 54247,
      "capacity_mw": 77819,
      "gert_p99_load_mw": 56771,
      "risk_score": 28.8
    },
    {
      "hour": 35,
      "timestamp_label": "Feb 15, 11:00",
      "temperature": 8,
      "actual_load_mw": 52325,
      "capacity_mw": 78500,
      "gert_p99_load_mw": 54625,
      "risk_score": 22
    }
  ],
  "logs": [
    {
      "hour": 4,
      "message": "Cold-weather watch initiated as the probabilistic tail widens.",
      "source": "GERT",
      "severity": "INFO"
    },
    {
      "hour": 11,
      "message": "P99 demand enters the two-gigawatt capacity buffer.",
      "source": "RISK",
      "severity": "WARNING"
    },
    {
      "hour": 17,
      "message": "Modeled tail crosses available capacity; reserve action indicated.",
      "source": "GERT",
      "severity": "CRITICAL"
    },
    {
      "hour": 23,
      "message": "Sustained generation outages constrain the recovery window.",
      "source": "OPS",
      "severity": "CRITICAL"
    },
    {
      "hour": 31,
      "message": "Capacity margin begins recovering as temperature pressure eases.",
      "source": "OPS",
      "severity": "INFO"
    }
  ],
  "provenance": "synthetic_reconstruction",
  "methodology_note": "Deterministic educational reconstruction; not an official historical event record."
};

export function onRequestGet() {
  return Response.json(PAYLOAD, {
    headers: { "cache-control": "no-store" },
  });
}
