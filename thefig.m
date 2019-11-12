function figures

close all;
data = csv2cell('dat.csv', 'fromfile');

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

% Just make one thing: for all remotes, plot FGU vs. workspace vs. SAT time
% Ignore unsat

numfgu = cellfun(@str2numNaN, data(2:end, 5));
satTime = cellfun(@str2numNaN, data(2:end,17));

% OK, workspace volume time.
wv = zeros(numel(data(2:end, 3)),1);
for i = 1:numel(data(2:end, 3))
    wv(i) = prod(sscanf(data{i+1,3}, '%d-%d-%d')); %count tot # cells
end

% 3-plot: FGU size, workspace size, SAT time

xlin = linspace(min(numfgu),max(numfgu),300);
ylin = linspace(min(wv),max(wv),300);
[X,Y] = meshgrid(xlin,ylin);
f = TriScatteredInterp(numfgu, wv, satTime);
Z = f(X,Y);
figure
fig = surf(X,Y,Z);
set(fig,'EdgeColor','none')
set(fig,'FaceLighting','gouraud')
daspect([1 1 1])
camlight left
title('FGU # vs. workspace volume vs. SAT time');

% Try a 3D bar chart
% columns are X
wvVec = unique(wv, 'sorted');
fguVec = unique(numfgu, 'sorted');
timeMat = zeros(numel(wvVec), numel(fguVec));
for c = 1:numel(fguVec)
   for r = 1:numel(wvVec)
      I = (numfgu == fguVec(c)) & (wv == wvVec(r));
      if I == 0
        timeMat(r,c) = 0;
      else
        timeMat(r,c) = mean(mean(satTime(I)));
      end
   end
end
fun = @(x) {num2str(x)};
xticks = cellfun(fun, num2cell(fguVec));
yticks = cellfun(fun, num2cell(wvVec));
figure;
fig = bar3(timeMat);
axis([0 numel(fguVec)+1 0 numel(wvVec)+1])
colormap parula
for k = 1:length(fig)
    zdata = get(fig(k),'ZData');
    set(fig(k),'CData', zdata);
    set(fig(k),'FaceColor', 'interp');
    if zdata == 0
        set(fig(k),'FaceColor', 'none');
    end
end
set(gca, 'XTickLabel', xticks)
set(gca, 'YTickLabel', yticks)
%title('FGU # vs. workspace volume vs. SAT time','FontSize', 14)
xlabel('FGU #','FontSize', 14)
ylabel('Workspace Volume','FontSize', 14)
zlabel('SAT Time','FontSize', 14)




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