// C26 endpoint-family enumeration. Imports no C20--C25 mathematical code.
#include <algorithm>
#include <array>
#include <iostream>
#include <set>
#include <stdexcept>
#include <string>
#include <vector>
#include <sys/resource.h>
#include <unistd.h>
using namespace std;
void need(bool b,const char*s){if(!b)throw runtime_error(s);}
struct G {
 int n,m;vector<pair<int,int>>E;vector<vector<int>>adj,nb;vector<array<int,4>>W;
 G(int n0,int m0):n(n0),m(m0),adj(n),nb(m){need(n>=1&&n<=10&&m>=1&&m<=15,"graph cap");set<pair<int,int>>seen;
 for(int e=0;e<m;e++){int a,b;need(bool(cin>>a>>b)&&0<=a&&a<b&&b<n,"edge endpoints");need(seen.insert({a,b}).second,"simple graph");E.push_back({a,b});adj[a].push_back(e);adj[b].push_back(e);}for(auto&a:adj)need(a.size()<=3,"subcubic");
 for(int e=0;e<m;e++)for(int f=0;f<m;f++)if(e!=f&&(E[e].first==E[f].first||E[e].first==E[f].second||E[e].second==E[f].first||E[e].second==E[f].second))nb[e].push_back(f);
 for(int s=0;s<n;s++){vector<int>v{s},es;walk(s,s,v,es);}set<unsigned>ids;for(auto s:W){unsigned z=0;for(int e:s)z|=1u<<e;need(ids.insert(z).second,"shape duplication");}}
 void walk(int s,int v,vector<int>&vs,vector<int>&es){if(es.size()==4){if(s<v)W.push_back({es[0],es[1],es[2],es[3]});return;}for(int e:adj[v]){int z=E[e].first^E[e].second^v;
 if(find(vs.begin(),vs.end(),z)==vs.end()){vs.push_back(z);es.push_back(e);walk(s,z,vs,es);es.pop_back();vs.pop_back();}
 else if(es.size()==3&&z==s&&s==*min_element(vs.begin(),vs.end())&&vs[1]<vs.back())W.push_back({es[0],es[1],es[2],e});}}
 bool connected(unsigned mask)const{if(!mask)return false;unsigned seen=1u<<__builtin_ctz(mask);vector<int>q{__builtin_ctz(mask)};for(size_t i=0;i<q.size();i++)for(int f:nb[q[i]])if((mask>>f&1)&&!(seen>>f&1)){seen|=1u<<f;q.push_back(f);}return seen==mask;}
 bool proper(const vector<int>&c)const{for(int e=0;e<m;e++)for(int f:nb[e])if(c[e]&&c[e]==c[f])return false;return true;}
 bool bichro(const vector<int>&c,const array<int,4>&s)const{return c[s[0]]&&c[s[1]]&&c[s[0]]==c[s[2]]&&c[s[1]]==c[s[3]];}
 int cost(const vector<int>&c)const{int v=0;for(auto s:W)v+=bichro(c,s);return v;}
 bool paths(const vector<int>&w,vector<vector<int>>&ps)const{unsigned left=0;vector<int>deg(n);for(int e=0;e<m;e++)if(!w[e]){left|=1u<<e;deg[E[e].first]++;deg[E[e].second]++;}if(*max_element(deg.begin(),deg.end())>2)return false;
 while(left){int first=__builtin_ctz(left);unsigned part=1u<<first;set<int>vs;vector<int>q{first};for(size_t i=0;i<q.size();i++){vs.insert(E[q[i]].first);vs.insert(E[q[i]].second);for(int f:nb[q[i]])if(!w[f]&&!(part>>f&1)){part|=1u<<f;q.push_back(f);}}if(q.size()>3||vs.size()!=q.size()+1)return false;
 int v=-1,ends=0;for(int z:vs)if(deg[z]==1){ends++;if(v<0)v=z;}if(ends!=2)return false;vector<int>p;unsigned used=0;for(size_t i=0;i<q.size();i++){int e=-1;for(int f:adj[v])if((part>>f&1)&&!(used>>f&1)){e=f;break;}need(e>=0,"path order");p.push_back(e);used|=1u<<e;v=E[e].first^E[e].second^v;}ps.push_back(p);left&=~part;}
 return true;}
 vector<int>decode(const vector<int>&w,const vector<vector<int>>&ps,int b)const{vector<int>c=w;for(size_t i=0;i<ps.size();i++)for(size_t j=0;j<ps[i].size();j++)c[ps[i][j]]=5+((b>>i&1)^(j%2));return c;}
 bool frame(const vector<int>&w,vector<vector<int>>&ps)const{return w.size()==size_t(m)&&all_of(w.begin(),w.end(),[](int x){return x>=0&&x<=4;})&&proper(w)&&cost(w)==0&&paths(w,ps);}
};
string digits(const vector<int>&a){string s;for(int x:a){need(x>=0&&x<=9,"digit bound");s+=char('0'+x);}return s;}
void ints(const vector<int>&a){cout<<'[';for(size_t j=0;j<a.size();j++){if(j)cout<<',';cout<<a[j];}cout<<']';}
struct Search {
 const G&g;vector<int>c,order,att;vector<vector<array<int,4>>>complete;vector<bool>ban;int best,target;bool early;unsigned S;long long leaves=0,nodes=0;
 Search(const G&a):g(a){}
 void rec(int t,int score){if(early&&best<target)return;nodes++;if(t==int(order.size())){leaves++;if(score<best){best=score;att=c;}return;}int e=order[t];for(int a=1;a<=6;a++){if(a>=5&&ban[e])continue;bool ok=true;for(int f:g.nb[e])if(c[f]==a){ok=false;break;}if(!ok)continue;c[e]=a;int add=0;
 for(auto w:complete[t])if(g.bichro(c,w)){if((c[w[0]]<=4)==(c[w[1]]<=4)){ok=false;break;}add++;}if(ok)rec(t+1,score+add);}c[e]=0;}
 void run(unsigned mask,const vector<int>&old,int threshold,bool stop){S=mask;c=old;target=threshold;early=stop;order.clear();att.clear();ban.assign(g.m,false);best=1000000;leaves=nodes=0;
 for(int e=0;e<g.m;e++)if(S>>e&1){order.push_back(e);for(int f:g.nb[e])if(!(S>>f&1)&&old[f]>=5)ban[e]=true;}
 sort(order.begin(),order.end(),[&](int a,int b){int da=0,db=0;for(int f:g.nb[a])da+=!(S>>f&1);for(int f:g.nb[b])db+=!(S>>f&1);return da!=db?da>db:a<b;});vector<int>pos(g.m,-1);complete.assign(order.size(),{});for(size_t i=0;i<order.size();i++)pos[order[i]]=i;int outside=0;
 for(auto w:g.W){int last=-1;for(int e:w)last=max(last,pos[e]);if(last<0)outside+=g.bichro(old,w);else complete[last].push_back(w);}for(int e:order)c[e]=0;rec(0,outside);need(leaves>0,"old endpoint absent");}
};
bool closed(unsigned s,const vector<vector<int>>&ps){for(auto&p:ps){int count=0;for(int e:p)count+=s>>e&1;if(count&&count!=int(p.size()))return false;}return true;}
void patch_table(const G&g,const vector<int>&w,int K){vector<vector<int>>ps;need(g.frame(w,ps),"old preframe");vector<int>costs,opt;int mu=100000;for(int b=0;b<(1<<ps.size());b++){costs.push_back(g.cost(g.decode(w,ps,b)));mu=min(mu,costs.back());}for(int b=0;b<int(costs.size());b++)if(costs[b]==mu)opt.push_back(b);
 cout<<"{\"verdict\":\"candidate_only\",\"word\":\""<<digits(w)<<"\",\"costs\":";ints(costs);cout<<",\"rows\":[";bool comma=false;Search q(g);
 for(int k=1;k<=K;k++)for(unsigned S=1;S<(1u<<g.m);S++)if(__builtin_popcount(S)==k&&g.connected(S)&&closed(S,ps))for(int b=0;b<int(costs.size());b++){q.run(S,g.decode(w,ps,b),mu,false);if(comma)cout<<',';comma=true;cout<<'['<<S<<','<<b<<','<<q.leaves<<','<<q.nodes<<','<<q.best<<",\""<<digits(q.att)<<"\"]";}
 cout<<"]}\n";}
struct Catalog {
 const G&g;int K;vector<int>w;bool comma=false;long long count=0;Catalog(const G&a,int bound):g(a),K(bound),w(g.m){}
 void collect(int used){vector<vector<int>>ps;if(!g.frame(w,ps))return;vector<int>costs,opt;int mu=100000;for(int b=0;b<(1<<ps.size());b++){costs.push_back(g.cost(g.decode(w,ps,b)));mu=min(mu,costs.back());}for(int b=0;b<int(costs.size());b++)if(costs[b]==mu)opt.push_back(b);
 unsigned found=0;int phase=opt[0];vector<int>endpoint=g.decode(w,ps,phase);Search q(g);
 if(mu)for(int k=1;k<=K&&!found;k++)for(unsigned S=1;S<(1u<<g.m)&&!found;S++)if(__builtin_popcount(S)==k&&g.connected(S)&&closed(S,ps))for(int b:opt){q.run(S,g.decode(w,ps,b),mu,true);if(q.best<mu){found=S;phase=b;endpoint=q.att;break;}}
 need(mu==0||found,"small graph family has no improvement");if(comma)cout<<',';comma=true;count++;long long orbit=1;for(int i=0;i<used;i++)orbit*=4-i;cout<<"[\""<<digits(w)<<"\","<<mu<<','<<orbit<<',';ints(costs);cout<<','<<found<<','<<phase<<",\""<<digits(endpoint)<<"\"]";}
 void gen(int e,int q){if(e==g.m){collect(q);return;}for(int a=0;a<=min(4,q+1);a++){bool ok=true;if(a)for(int f:g.nb[e])if(f<e&&w[f]==a){ok=false;break;}if(!ok)continue;w[e]=a;
 for(auto s:g.W)if(*max_element(s.begin(),s.end())==e&&g.bichro(w,s)){ok=false;break;}if(ok)gen(e+1,max(q,a));}w[e]=0;}
 void run(){need(g.n<=6&&g.m<=9,"catalog finite scope");cout<<"{\"verdict\":\"candidate_only\",\"states\":[";gen(0,0);cout<<"],\"count\":"<<count<<"}\n";}
};
int main(){try{alarm(35);rlimit cpu{30,31},memory{805306368,805306368},files{4194304,4194304};setrlimit(RLIMIT_CPU,&cpu);setrlimit(RLIMIT_AS,&memory);setrlimit(RLIMIT_FSIZE,&files);string mode;int n,m,K;need(bool(cin>>mode>>n>>m>>K)&&K>=1&&K<=5,"request");need(n>=1&&n<=10&&m>=1&&m<=15,"graph cap before allocation");G g(n,m);if(mode=="catalog"){Catalog t(g,K);t.run();}else{need(mode=="patches","mode");vector<int>w(m);for(int&i:w)need(bool(cin>>i),"word");patch_table(g,w,K);}return 0;}catch(const exception&e){cerr<<e.what()<<'\n';return 2;}}
