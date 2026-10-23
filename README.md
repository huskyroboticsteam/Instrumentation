# Instrumentation

Code and documentation for the Husky Robotics Instrumentation subteam, University of Washington

We build the onboard instruments that analyze soil for signs of life. The current focus is a camera-based spectrometer: a Raspberry Pi camera photographs light that has passed through a test sample, and our code turns that photo into a spectrum. 


## Sofware setup

## Data format
Each frame is reduced to a CSV with one row per pixel column.
| Column | Meaning |
|---|---|
| `pixel` | column index across the sensor (0 = left edge) |
| `raw_intensity` | average brightness of that column |
| `intensity_0_to_1` | raw intensity divided by the brightest column |
| `wavelength_nm` | added once the instrument is calibrated |
 
Use `raw_intensity` when **comparing samples**. The 0 to 1 column is scaled per frame, so it shows the shape of a spectrum but hides overall brightness differences between frames.
