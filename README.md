# Refactoring Python_Classes for NSLS-II Beamlines
This repo is a collection of all the work done towards consolidating Ophyd classes for NSLS-II profile collection repos at Brookhaven National Laboratory. This project was supported in part by the U.S. Department of Energy, Office of Science, Office of Workforce Development for Teachers and Scientists (WDTS) under the Community College Internships Program (CCI).

Abstract:

The National Synchrotron Light Source II (NSLS-II) is one of the most advanced synchrotron light sources in the world, where many important scientific discoveries. With many of the beamlines offering unique experimental capabilities, researchers can probe materials, biological systems, and chemical processes at unparalleled resolution. Despite these differences, many beamlines rely on similar underlying software, which has led to duplication of code across instruments. This creates long-term maintenance and reliability challenges. This project addresses that issue by refactoring and consolidating Ophyd classes, a Python library used to control devices at the beamlines. By unifying similar classes into a single, reusable, and maintainable package, the project enhances code readability, portability, and supportability. This work supports NSLS-II’s mission to provide robust tools for scientific discovery. 

What this repo includes:
- An AI assited aproach that used cosine similairty and clustering to consolidate Ophyd classes (look into ophyd-class-grouping).
- A deterministic approach for consolidation using Jaccard analysis (files present upon opening the repo, numbered 1-4).
- Artifacts produced from both approaches including graphs, JSON files, etc. 
- Project poster presentation, slidshow, and report paper.

How this repo works:

This repo is supposed to work with the profile collection repositories from NSLS-II. So a local chechout of all available repos is necessary. 

To use the approach without AI, you will need to add 01_ophyd_class_collection.py into the directory where all the profile collection repos are located. 

After, you can begin to insert the following files numbered 2-4 to reproudce the artifacts. 

Anyways, the previous artifacts are here on this github. 

THINGS TO NOTE:

- Yes, most of the files use class_details5.json. This would imply that other JSON files came before that one. That is true. All the files (except for the AI ones), use class_details5.json. An output from 01_ophyd_class_collection.py would produce the same output as class_details5.json as of 10/31/2025. 

- AI files need an OpenAI API key. 