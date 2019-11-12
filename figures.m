function figures

close all;
data = csv2cell('log.csv', 'fromfile');

%  TODO problem build time + SAT time, and completion rate YY

% Columns:
% 1 - Timestamp (time test was run)
% 2 - Schematic (name of problem; if not random, name is unique)
% 3 - Workspace 
% 4 - Bitlbox #
% 5 - FGU #
% 6 - Connection #
% 7 - Uniqueness clauses
% 8 - Uniqueness time
% 9 - Collision clauses
% 10 - Collision time
% 11 - Short clauses
% 12 - Short time
% 13 - Connection clauses
% 14 - Connection time
% 15 - Fixed Bitblox
% 16 - MemError
% 17 - SAT Time
% 18 - SAT

numbitblox = cellfun(@str2numNaN, data(2:end, 4));
numfgu = cellfun(@str2numNaN, data(2:end, 5));
satTime = cellfun(@str2numNaN, data(2:end,17)); %NOTE: Anthony, we should change this to ignore SAT times when the Problem is unsat
% You mean set them to something like 0 or inf? We need to preserve length
% of vector for plotting purposes. I settled on NaN because it does not
% plot.
SAT = cellfun(@str2numNaN, data(2:end,18));


uniquefgu = unique(numfgu);    %the unique fgu instances (since many tests have the same # of fgus
for i = 1:length(uniquefgu)
    fguinst_index = find(numfgu==uniquefgu(i));
    uniquefgusatpct(i) = nansum(SAT(fguinst_index))/length(fguinst_index);   %the percent of those fgu instances that were satisfied
end

uniquebitblox = unique(numbitblox);    %the unique bitblox instances (since many tests have the same # of fgus
for i = 1:length(uniquebitblox)
    bbinst_index = find(numbitblox==uniquebitblox(i));
    uniquebbsatpct(i) = nansum(SAT(bbinst_index))/length(bbinst_index);   %the percent of those bitblox instances that were satisfied
end


% Take a look at FGU # vs. SAT time
plot(numfgu,satTime,'X');
title('FGU # vs. SAT solver time');

% FGU vs. problem building time
uniqueTime = cellfun(@str2numNaN, data(2:end, 8));
collisionTime = cellfun(@str2numNaN, data(2:end, 10));
shortTime = cellfun(@str2numNaN, data(2:end, 12));
connectionTime = cellfun(@str2numNaN, data(2:end, 14));
problemTime = uniqueTime + collisionTime + shortTime + connectionTime;
figure; plot(numfgu, problemTime,'X');
title('FGU # vs. problem build time');

% For FGU up to 192, plot average SAT time per FGU
fguCount = [];
fguAve = [];
for i = 8:8:192
   fguCount = [fguCount i];
   fguAve = [fguAve mean(unnan(satTime(~isnan(numfgu)&(numfgu == i))))];
end
figure; plot(fguCount, fguAve, 'X');
title('FGU # vs. average SAT time for that #');

% What about number of Bitblox?
bbNum = cellfun(@str2numNaN, data(2:end, 4));
figure; plot(bbNum, satTime, 'X');
title('Bitblox # vs. SAT time');

% And its average?
bbNumI = 2:16;
bbAve = bbNumI;
for i = 2:16
    bbAve(i-1) = mean(unnan(satTime((bbNum == i))));
end
figure; plot(bbNumI, bbAve, 'X');
title('Bitblox # vs. average SAT time for that #');

% OK, workspace volume time.
wv = zeros(numel(data(2:end, 3)),1);
for i = 1:numel(data(2:end, 3))
    wv(i) = prod(sscanf(data{i+1,3}, '%d-%d-%d')); %count tot # cells
end
figure; plot(wv, satTime, 'X');
title('Workspace volume vs. SAT time');

% Hmm... new metric, "Connection density", connections/BB
connections = cellfun(@str2numNaN, data(2:end, 6));
density = connections./bbNum;
figure; plot(density,satTime,'X');
title('Connection density vs. SAT time');

% 3-plot: FGU size, workspace size, SAT time
figure; plot3(numfgu, wv, satTime, 'X');
title('FGU # vs. workspace volume vs. SAT time');

% 2 Y axis-plot: FGU size vs total time & FGU size vs percent satisfied
i=find(uniquefgu<200);
figure; [hAx,hLine1,hLine2] = plotyy(numfgu, satTime+problemTime, uniquefgu(i), uniquefgusatpct(i));
title('#FGU vs. Time & Percent SAT');
set(hLine1,'LineStyle', 'none', 'Marker', 'x');
set(hLine2,'LineStyle', 'none', 'Marker', 'o');
xlabel('Number of FGUs')
ylabel(hAx(1),'Total Time (sec)') % left y-axis
ylabel(hAx(2),'Percent Satisfied') % right y-axis
set(hAx(1),'YTick',linspace(0,500,6));
set(hAx(2),'YTick',linspace(0,1,11));

% 2 Y axis-plot: Bitblox size vs total time & Bitblox size vs percent satisfied
i=find(uniquebitblox<20);
figure; [hAx,hLine1,hLine2] = plotyy(numbitblox, satTime+problemTime, uniquebitblox(i), uniquebbsatpct(i));
title('#Bitblox vs. Time & Percent SAT');
set(hLine1,'LineStyle', 'none', 'Marker', 'x');
set(hLine2,'LineStyle', 'none', 'Marker', 'o');
xlabel('Number of Bitblox')
ylabel(hAx(1),'Total Time (sec)') % left y-axis
ylabel(hAx(2),'Percent Satisfied') % right y-axis
set(hAx(1),'YTick',linspace(0,500,6));
set(hAx(2),'YTick',linspace(0,1,11));





function out = str2numNaN(in)
if isempty(in)
    out = NaN;
else
    in = strtrim(in);
    if isempty(in)
        out = NaN;
        return
    end
    out = str2num(in);
end

function out = unnan(in)
    out = in(~isnan(in));