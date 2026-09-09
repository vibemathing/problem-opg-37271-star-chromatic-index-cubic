// C24: complete preframe reconfiguration by color-prefix enumeration.
// No previous compiler/checker imported. CPU/memory/output caps: companion runner.
#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <fstream>
#include <functional>
#include <iostream>
#include <map>
#include <queue>
#include <set>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>
using namespace std;
using Word=array<int,15>;
struct State {uint64_t code;Word w;int mu,phase;};
int n,m; vector<pair<int,int>> E;array<uint32_t,15> nearEdge;vector<State> S;unordered_map<uint64_t,int> indexOf;
void need(bool b,const string&s){if(!b)throw runtime_error(s);}
uint64_t encode(const Word&w){uint64_t z=0;for(int i=0;i<m;i++)z=5*z+w[i];return z;}
uint64_t canonical(const Word&w){int labels[7]={0},next=0;uint64_t z=0;for(int i=0;i<m;i++){int c=w[i];if(c&&!labels[c])labels[c]=++next;z=5*z+labels[c];}return z;}
uint32_t component(uint32_t mask,int e){uint32_t part=1u<<e,front=part;while(front){int f=countr_zero(front);front&=front-1;uint32_t add=mask&nearEdge[f]&~part;part|=add;front|=add;}return part;}
vector<vector<int>> upaths(const Word&w,int len){
 uint32_t mask=0;for(int e=0;e<len;e++)if(w[e]==0)mask|=1u<<e;
 vector<vector<int>> out;
 while(mask){int e=countr_zero(mask);uint32_t part=component(mask,e);mask&=~part;int ct=popcount(part);if(ct>3)return {{-1}};
  int deg[10]={0};for(int f=0;f<m;f++)if(part>>f&1){deg[E[f].first]++;deg[E[f].second]++;}
  int v=-1,ends=0,vertices=0;for(int a=0;a<n;a++){if(deg[a]>2)return {{-1}};vertices+=(deg[a]>0);if(deg[a]==1){ends++;if(v<0)v=a;}}
  if(ends!=2||vertices!=ct+1)return {{-1}};
  vector<int> path;uint32_t rem=part;while(rem){int f=0;while(f<m&& (!(rem>>f&1)||(E[f].first!=v&&E[f].second!=v)))f++;need(f<m,"path traversal");path.push_back(f);v=E[f].first^E[f].second^v;rem&=~(1u<<f);}out.push_back(path);
 }return out;
}
bool old_safe(const Word&w,int e){int a=w[e];for(int f=0;f<e;f++)if((nearEdge[e]>>f&1)&&w[f]==a)return false;
 for(int b=1;b<=4;b++)if(a!=b){uint32_t mask=0;for(int f=0;f<=e;f++)if(w[f]==a||w[f]==b)mask|=1u<<f;if(popcount(component(mask,e))>3)return false;}return true;}
int violations(const Word&w){int total=0;
 for(int a=1;a<=4;a++)for(int b=5;b<=6;b++){uint32_t mask=0;for(int e=0;e<m;e++)if(w[e]==a||w[e]==b)mask|=1u<<e;
  while(mask){uint32_t part=component(mask,countr_zero(mask));mask&=~part;int ct=popcount(part);if(ct<4)continue;uint32_t vs=0;for(int e=0;e<m;e++)if(part>>e&1)vs|=(1u<<E[e].first)|(1u<<E[e].second);
   total+=(popcount(vs)==ct)?(ct==4?1:ct):ct-3;
  }
 }return total;
}
uint64_t phase_trials=0,raw_frames=0,raw_phases=0;
void enumerate(){Word w{};
 function<void(int,int)> visit=[&](int pos,int used){
  if(pos==m){auto paths=upaths(w,m);need(paths.empty()||paths[0][0]>=0,"leaf topology");int best=100000,bphase=-1;
   for(int phase=0;phase<(1<<(int)paths.size());phase++){Word full=w;for(int j=0;j<(int)paths.size();j++)for(int p=0;p<(int)paths[j].size();p++)full[paths[j][p]]=5+((phase>>j&1)^(p&1));int cost=violations(full);if(cost<best){best=cost;bphase=phase;}phase_trials++;}
   uint64_t orbit=1;for(int j=0;j<used;j++)orbit*=4-j;raw_frames+=orbit;raw_phases+=orbit*(1<<paths.size());S.push_back({encode(w),w,best,bphase});need(S.size()<=2000000,"state cap");return;
  }
  for(int a=0;a<=min(4,used+1);a++){w[pos]=a;
   if(a==0){auto paths=upaths(w,pos+1);if(!paths.empty()&&paths[0][0]<0)continue;}
   else if(!old_safe(w,pos))continue;
   visit(pos+1,max(a,used));
  }w[pos]=0;
 };visit(0,0);sort(S.begin(),S.end(),[](auto&a,auto&b){return a.code<b.code;});for(int i=0;i<(int)S.size();i++)need(indexOf.emplace(S[i].code,i).second,"duplicate state");
}
vector<int> neighbors(int i){vector<int> out;Word w=S[i].w;for(int e=0;e<m;e++){int old=w[e];for(int a=0;a<=4;a++)if(a!=old){w[e]=a;auto it=indexOf.find(canonical(w));if(it!=indexOf.end()&&it->second!=i)out.push_back(it->second);}w[e]=old;}sort(out.begin(),out.end());out.erase(unique(out.begin(),out.end()),out.end());return out;}
int main(int argc,char**argv){try{
 need(argc==3,"usage: space graph.txt output-prefix");ifstream in(argv[1]);in>>n>>m;need(n>=4&&n<=10&&m==3*n/2&&m<=15,"graph cap");int d[10]={0};set<pair<int,int>> seen;
 for(int e=0;e<m;e++){int a,b;in>>a>>b;need(in.good()&&a>=0&&b>=0&&a<n&&b<n&&a<b&&seen.insert({a,b}).second,"simple edge input");E.push_back({a,b});d[a]++;d[b]++;}need(all_of(d,d+n,[](int v){return v==3;}),"cubic");
 for(int e=0;e<m;e++)for(int f=0;f<m;f++)if(e!=f&&(E[e].first==E[f].first||E[e].first==E[f].second||E[e].second==E[f].first||E[e].second==E[f].second))nearEdge[e]|=1u<<f;
 enumerate();int N=S.size();vector<vector<int>> adj(N);for(int i=0;i<N;i++)adj[i]=neighbors(i);
 vector<int> block(N,-1),parent(N,-1),dist(N,-1);queue<int> q;for(int i=0;i<N;i++)if(S[i].mu==0){q.push(i);dist[i]=0;parent[i]=i;}
 while(!q.empty()){int i=q.front();q.pop();for(int j:adj[i])if(dist[j]<0&&S[j].mu>=S[i].mu){dist[j]=dist[i]+1;parent[j]=i;q.push(j);}}
 string prefix=argv[2];ofstream blocks(prefix+".blocks");int bid=0,closed=0;map<int,int> hist;
 for(int i=0;i<N;i++){hist[S[i].mu]++;if(S[i].mu==0||block[i]>=0)continue;vector<int> part;block[i]=bid;q.push(i);int exits=0;uint64_t firstExit=0,firstLower=0;
  while(!q.empty()){int a=q.front();q.pop();part.push_back(a);bool exit=false;for(int b:adj[a]){if(S[b].mu<S[a].mu){exit=true;if(!firstExit){firstExit=S[a].code;firstLower=S[b].code;}}if(S[b].mu==S[a].mu&&block[b]<0){block[b]=bid;q.push(b);}}exits+=exit;}
  blocks<<bid<<' '<<S[i].mu<<' '<<part.size()<<' '<<exits<<' '<<firstExit<<' '<<firstLower<<'\n';if(!exits){closed++;ofstream sink(prefix+".closed-"+to_string(bid));sort(part.begin(),part.end());for(int j:part)sink<<S[j].code<<'\n';}bid++;
 }
 ofstream states(prefix+".states");for(int i=0;i<N;i++)states<<S[i].code<<' '<<S[i].mu<<' '<<S[i].phase<<' '<<(parent[i]<0?uint64_t(-1):S[parent[i]].code)<<' '<<dist[i]<<' '<<block[i]<<'\n';
 cout<<"{\"n\":"<<n<<",\"states\":"<<N<<",\"raw_frames\":"<<raw_frames<<",\"phase_trials\":"<<phase_trials<<",\"raw_phase_trials\":"<<raw_phases<<",\"positive_blocks\":"<<bid<<",\"closed_blocks\":"<<closed<<",\"unreachable\":"<<count(dist.begin(),dist.end(),-1)<<",\"max_distance\":"<<*max_element(dist.begin(),dist.end())<<",\"mu_histogram\":{";bool first=true;for(auto [v,c]:hist){if(!first)cout<<',';first=false;cout<<'"'<<v<<"\":"<<c;}cout<<"},\"verdict\":\"candidate_only\"}\n";
 return 0;
 }catch(const exception&e){cerr<<e.what()<<'\n';return 2;}}
