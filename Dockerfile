FROM python:3.6

# --------------------------------------------------------------------------------------------
# Install Cytomine python client
RUN git clone https://github.com/cytomine-uliege/Cytomine-python-client.git
RUN cd /Cytomine-python-client && git checkout tags/v2.2.0 && pip install .
RUN rm -r /Cytomine-python-client

# --------------------------------------------------------------------------------------------
# Install Neubias-W5-Utilities (annotation exporter, compute metrics, helpers,...)
RUN git clone https://github.com/Neubias-WG5/neubiaswg5-utilities.git
RUN cd /neubiaswg5-utilities/ && git checkout tags/v0.5.2a && pip install .

# Metric for TreTrc is DIADEM.jar so it needs java
RUN apt-get update && apt-get install openjdk-8-jdk -y && apt-get cleandock
# RUN chmod +x /neubiaswg5-utilities/bin/*
# RUN cp /neubiaswg5-utilities/bin/* /usr/bin/
# RUN rm -r /neubiaswg5-utilities

# the code to download DiademMetric is below, need to discuss
# with team to check how to manage using it in compute_metrics.py
# RUN wget http://diademchallenge.org/docs/DiademMetric.tar
# RUN tar -xvf DiademMetric.tar 
# RUN rm ExampleGoldStandard.swc ExampleTest.swc api.txt readme.txt

# --------------------------------------------------------------------------------------------
# Install needed packages to run rivuletpy as per https://github.com/RivuletStudio/rivuletpy
RUN pip install matplotlib cython tqdm libtiff scikit-fmm simpleITK
RUN pip install git+https://github.com/pearu/pylibtiff.git
RUN git clone https://github.com/RivuletStudio/rivuletpy.git
RUN cd rivuletpy && python setup.py install
RUN pip install .
# --------------------------------------------------------------------------------------------
# Install scripts and models
ADD descriptor.json /app/descriptor.json
ADD wrapper.py /app/wrapper.py
ADD swc_to_tiff_stack.py /app/swc_to_tiff_stack.py 

ENTRYPOINT ["python", "/app/wrapper.py"]