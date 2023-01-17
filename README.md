# T1 Thermal Testing
Python 3.10.8

I did thermal testing for different fan layouts, side panels (changing CPU side only), and top panels, and have conveniently plotted all the results.  
All the results are normalised to an ambient temperature of 22°C.  
# Hardware  
I run my FormD T1 v2 sandwich case in 2 slot mode, PSU in alternative 90° mount, aluminium side panel on GPU side, with the following hardware:  

* 5900x (PPT 160W, TDC 150A, EDC, 190A + CO values)  
* 3080 FE (undervolted)  
* 2x16 GB 3600 c16 Crucial RGB ram  
* Asus B550i strix motherboard  
* Corsair SF750  
* Phanteks Glacier One 240MP  
* 2 pin thermal probe taped to radiator tank and attached to the motherboard for liquid temp readings  
  
# Test parameters
### [Side panel:](https://imgur.com/LURjMbH)  
* [Aluminium](https://imgur.com/K7qZbpJ)  
* [Acrylic mesh](https://imgur.com/vwnjcuq)  
* [Tempered glass \(TG\)](https://imgur.com/2Uk37Uu)  

### [Top panel:](https://imgur.com/U21fTno)  
* [Stock](https://imgur.com/9eB72TU)  
* [Acrylic mesh](https://imgur.com/O7XTDP3)  
* [Hollow](https://imgur.com/OjFol68) (the mesh of the [acrylic mesh](https://imgur.com/zhp1k5X) is removable)    

### Fan combinations:  
I do not have the ability to do noise normalised testing, so I kept fan speeds constant. For the Noctua A12x25 and Phanteks T30 (advanced mode) I matched their fan speeds. The Noctua A12x15 speed is my personal noise limit for the slim fan, above this I find the sound unpleasant.  
The A12x15 was always run at 75%, ~1430 rpm  
The A12x25 was always run at 86%, ~1750 rpm  
The T30 was always run at 60%, ~1750 rpm  

* A12x15 + T30  
* A12x15 + A12x25  
* A12x25 + T30  

# Tests:  
For each configuration I ran:  

* Cinebench R23 for 10 minutes, just to get some heat in the loop.
* The same Cyperpunk 2077 save file, with a mix of high and ultra settings, and ray tracing enabled, for 15 minutes. I focus on these results for the conclusions.  
* OCCT Power test, which loads 100% of the power limit for both CPU and GPU, for 15 minutes. Keep in mind this is an unrealistic test, practically no real workload will ever run under these conditions, this is a worst case scenario.  

# Results:  
[Full album here](https://imgur.com/a/iRgDeBt)  
#### [Cinebench R23:](https://imgur.com/kUNYo8w)   
We see relatively little scaling here in terms of CPU temperature, but a ~5°C difference in liquid temperatures from best to worst.  
#### [Cyberpunk 2077:](https://imgur.com/qAaFhDU)   
CPU & GPU temperatures stay under control regardless of the configuration, we see a ~10°C difference in liquid temperatures from best to worst. I focus on these results.  
#### [OCCT:](https://imgur.com/EV6z5VZ)   
Same story as Cyberpunk, CPU and GPU temperatures are reasonable, and a ~11°C difference in liquid temperatures.  

# Conclusions:  
**All conclusions here focus on the gaming testing and are based on my setup, with a thicker GPU, an air cooling setup, or any other changes your results might differ.**  
### Side panels:

* Acrylic mesh side panel performs within margin of error to the aluminium side panel.  
* With the stock top panel, the tempered glass side panel increases CPU temperatures by 3°C, but decreases GPU temperatures by 3°C. It negatively impacts liquid temperatures and increases them by 3°C.  The improvement in GPU temperatures is likely because more air is forced through the GPU compartment.  
With the hollow and acrylic mesh top panels, the gap is smaller, CPU increases only 1-2°C, liquid temperature increases ~2°C, and GPU temperature drops ~2°C.  
* The aluminium and acrylic mesh side panels perform the best.

### Top panels:  
* The difference between the stock top panel and the acrylic mesh are marginal. Swapping to the acrylic mesh drops just over 1°C on the CPU, does not affect GPU temperatures, and drops 0.5°C on the liquid temperature.  
* The hollow top panel differences were more substantial. Compared to the stock top panel & aluminium side panel we see a 4°C drop in CPU temperatures, just over 1°C less on the GPU, and a 4°C drop in liquid temperatures. These differences are greater still in the power virus test.
* The hollow top panel performs the best, followed by the acrylic mesh, which is closely followed by the stock top panel.  

### Fan combinations:  
* I want to point to previous testing of mine, that shows how the combination of A12x15 + T30 outperforms a setup with 2 A12x15 + A T30, and how 2 slim fans is significantly worse, you can find this [here](https://www.reddit.com/r/FormD/comments/w7t7r4/aio_fan_testing_for_t1_v2_sandwich_layout/).
* Keeping the slim fan (A12x15) the same and substituing the T30 for the A12x25 and the stock panel we see identical or increased CPU temperatures, a slight improvent in GPU temperatures, but worsened liquid temperatures. The difference is not large, but the T30 does outperform the A12x25. However with the hollow top panel, the gap between the the A12x25 and T30 widens, we now see almost 2°C better liquid temperatures.  
* The hollow top panel allows for "hotrodding" [\(picture\)](https://imgur.com/jMT5BWs), where the radiator/fan area is expanded as it is no longer contained by the top panel. This allows you to use a non-slim fan on the motherboard side of the case. This leads to the A12x25 + T30 config. This improves temperature substantially, but keep in mind that not only is the A12x25 is a better fan than the A12x15, but it is spinning 300 RPM faster to match the T30 fan speed. Switching from the slim fan to the A12x25 drops CPU temperatures by 2°C, liquid temperatures by over 3°C, and GPU temperatures decrease by 0.5°C.  

### Stand:
* Stand testing [\(results\)](https://imgur.com/a/9iaZL0d) was not part of the testing procedures above, as I have tested it previously. The timespy graphics test was looped for 30 minutes, temperatures were within margin of between the standard and vertical mount.  
  
# Other information:  
* [Here](https://imgur.com/a/8NPrbwA) you can see pictures of the various setups, side panels, top panels, other bits.  
* [Here](https://imgur.com/a/OXfXxuf) you can see an ugly plot showing the temperature sensor, CPU temperature, GPU temperature, CPU package power, CPU fan speed (above motherboard), Chassis1 fan speed (above PSU), GPU Fan1, and GPU power for all 11 configurations over time, for each test.  
* [Here](https://github.com/scottsimply/T1_Thermal_Testing) you can find the original data, as well as the code I use to import the HWINFO64 CSVs and plot the data.
  
# TL;DR:  
* TG side panel increases CPU and liquid temperatures by 2-3°C, but decreases GPU temperatures by the same.  
* Acrylic mesh and aluminium side panel perform identically.  
* The acrylic mesh top panel is marginaly better than the stock top panel, the hollow top panel performs best.  
* T30 + A12x15 is the best AIO fan setup (excluding SW Pro 4).  
* Hotrodding with the hollow top panel gives a lot more thermal headroom.
* The stand does not affect temperatures.
